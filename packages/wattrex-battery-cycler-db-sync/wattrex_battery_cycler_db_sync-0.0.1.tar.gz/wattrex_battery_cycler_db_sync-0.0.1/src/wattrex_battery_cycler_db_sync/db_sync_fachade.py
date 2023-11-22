#!/usr/bin/python3
'''
_______________________________________________________________________________
'''

#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations # pylint: disable=wrong-import-position
from typing import List
from sys import path
import os

#######################         GENERIC IMPORTS          #######################

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
path.append(os.getcwd())
from system_logger_tool import SysLogLoggerC, sys_log_logger_get_module_logger # pylint: disable=wrong-import-position
if __name__ == '__main__':
    cycler_logger = SysLogLoggerC(file_log_levels='./log_config.yaml')
log = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################
from wattrex_driver_db import (DrvDbSqlEngineC, DrvDbTypeE, DrvDbAlarmC, DrvDbCacheExperimentC, # pylint: disable=wrong-import-position
                DrvDbCacheStatusC, DrvDbCacheExtendedMeasureC, DrvDbCacheGenericMeasureC,
                DrvDbMasterGenericMeasureC, DrvDbMasterExtendedMeasureC, DrvDbExpStatusE,
                DrvDbMasterStatusC, DrvDbMasterExperimentC, transform_experiment_db,
                transform_ext_meas_db, transform_gen_meas_db, transform_status_db)
#######################          MODULE IMPORTS          #######################

#######################              ENUMS               #######################

#######################              CLASSES             #######################

class DbSyncFachadeC(): # pylint: disable=too-many-instance-attributes
    '''It is a thread that runs in background and is used to synchronize
    the database with the other nodes.
    '''
    def __init__(self, cred_file:str):
        log.info("Initializing DB Connection...")
        #Remote database
        self.__master_db: DrvDbSqlEngineC = DrvDbSqlEngineC(db_type=DrvDbTypeE.MASTER_DB,
                                                            config_file= cred_file)
        #Local database
        self.__cache_db: DrvDbSqlEngineC = DrvDbSqlEngineC(db_type=DrvDbTypeE.CACHE_DB,
                                                            config_file= cred_file)
        self.__push_gen_meas: List[DrvDbCacheGenericMeasureC]  = []
        self.__push_ext_meas: List[DrvDbCacheExtendedMeasureC]  = []
        self.__push_status:   List[DrvDbCacheStatusC] = []
        self.__push_alarms:   List[DrvDbAlarmC] = []
        self.__push_exps:     List[DrvDbCacheExperimentC]   = []
        self.__last_exp_status: dict[int, DrvDbExpStatusE] ={}


    def push_gen_meas(self) -> None:
        '''Push the measures to the database.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        log.info("Pushing general measures...")
        cache_meas  = self.__cache_db.session.query(DrvDbCacheGenericMeasureC).all()
        for meas in cache_meas:
            if meas not in self.__push_gen_meas:
                meas_add = DrvDbMasterGenericMeasureC()
                transform_gen_meas_db(source= meas, target= meas_add)
                self.__push_gen_meas.append(meas)
                self.__master_db.session.add(meas_add)

    def push_ext_meas(self) -> None:
        '''Push the measures to the database.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        self.__cache_db.session.expire_all()
        log.info("Pushing external measures...")
        cache_meas = self.__cache_db.session.query(DrvDbCacheExtendedMeasureC).all()
        for meas in cache_meas:
            if meas not in self.__push_ext_meas:
                meas_add = DrvDbMasterExtendedMeasureC()
                transform_ext_meas_db(source= meas, target= meas_add)
                self.__push_ext_meas.append(meas)
                self.__master_db.session.add(meas_add)

    def push_alarms(self) -> None:
        '''Push the alarms to the database.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        log.info("Pushing alarms...")
        cache_meas = self.__cache_db.session.query(DrvDbAlarmC).all()
        for meas in cache_meas:
            if meas not in self.__push_alarms:
                self.__push_alarms.append(meas)
                self.__master_db.session.add(meas)


    def push_status(self) -> None:
        '''Push the status to the database.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        log.info("Pushing status...")
        cache_meas = self.__cache_db.session.query(DrvDbCacheStatusC).all()
        for meas in cache_meas:
            if meas not in self.__push_status:
                meas_add = DrvDbMasterStatusC()
                transform_status_db(source= meas, target= meas_add)
                self.__push_status.append(meas)
                self.__master_db.session.add(meas_add)

    def push_experiments(self) -> None:
        '''Push the experiments to the database.
        '''
        log.info("Pushing experiments...")
        cache_meas = self.__cache_db.session.query(DrvDbCacheExperimentC).all()
        for meas in cache_meas:
            meas_add = DrvDbMasterExperimentC()
            if (meas.ExpID not in self.__last_exp_status or (meas.ExpID in self.__last_exp_status
                and meas.Status != self.__last_exp_status[meas.ExpID])):
                self.__last_exp_status[meas.ExpID] = meas.Status
                log.info(f"Experiment {meas.ExpID} status changed to {meas.Status}")
                transform_experiment_db(source= meas, target= meas_add)
                self.__push_exps.append(meas)
                self.__master_db.session.merge(meas_add)

    def commit(self) -> None:
        '''Confirm the changes made to the indicated database.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        log.info("Commiting changes...")
        self.__master_db.commit_changes(raise_exception= True)
        ## No rollback done in master db

    def delete_pushed_data(self):
        '''Remove the pushed data from the cache database.
        '''
        for meas,name in zip([self.__push_alarms, self.__push_status,
                        self.__push_ext_meas, self.__push_gen_meas, self.__push_exps],
                        ['alarms', 'status', 'ext_meas', 'gen_meas', 'exps']):
            log.info(f"Deleting {name}...")
            for row in meas:
                self.__cache_db.session.expunge(row)
                self.__cache_db.session.delete(row)
            self.__cache_db.commit_changes(raise_exception= True)

        self.__push_gen_meas   = []
        self.__push_ext_meas   = []
        self.__push_status     = []
        self.__push_alarms     = []
        self.__push_exps       = []
