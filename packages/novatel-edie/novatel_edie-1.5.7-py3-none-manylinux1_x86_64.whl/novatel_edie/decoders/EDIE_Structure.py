from ctypes import *

# Patch c_bool be 4 bytes in size
temp_c_bool = c_bool
c_bool = c_uint32


class BaseStructMixin(object):
    def __getitem__(self, item):
        return self._fields_[item][0]

    def __str__(self):
        return ','.join([str(x) for x in self._fields_to_list()])

    def _fields_to_list(self):
        message_values = []
        fields = enumerate(self._fields_)
        for idx, (field_name, field_type) in fields:
            if hasattr(field_type, '_length_'):
                if field_type._type_ == c_char:
                    message_values.append(getattr(self, field_name))
                else:
                    for i in range(getattr(field_type, '_length_')):
                        message_values.append(getattr(self, field_name)[i])
            else:
                message_values.append(getattr(self, field_name))

                if field_name.endswith('_arraylength'):
                    array_len = getattr(self, field_name)
                    array_idx, (array_name, array_type) = next(fields)
                    array = getattr(self, array_name)
                    for i in range(array_len):
                        message_values.append(array[i])
        return message_values


class satelliteid(Structure, BaseStructMixin):
    _fields_ = [
                ("usPrnOrSlot", c_ushort),
                ("sFrequencyChannel", c_short),
                ]


# noinspection PyTypeChecker
class LOGLIST_LogList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("LogBaseInfo_LogPortAddress", c_uint),
                ("LogBaseInfo_MessageId", c_ulong),
                ("LogClass_Trigger", c_uint),
                ("LogClass_OnTime", c_double),
                ("LogClass_Offset", c_double),
                ("LogClass_Hold", c_uint),
                ]


# noinspection PyTypeChecker
class LOGLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("LogList_arraylength", c_ulong),
                ("LogList", LOGLIST_LogList*80),
                ]


# noinspection PyTypeChecker
class RTCAOBS_clMyRTCAOBS_TransmitterData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("L1LockFlag", c_char),
                ("L2LockFlag", c_char),
                ("L1PseudorangeOffset", c_double),
                ("L2PseudorangeOffset", c_double),
                ("L1ADROffset", c_float),
                ("L2ADROffset", c_float),
                ("L2NotEncrypted", c_bool),
                ("Reserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCAOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAOBS_NovAtelDesignator", c_char),
                ("clMyRTCAOBS_SubtypeIndicator", c_char),
                ("clMyRTCAOBS_MinimumPseudorange", c_double),
                ("clMyRTCAOBS_Seconds", c_float),
                ("clMyRTCAOBS_Reserved", c_int),
                ("clMyRTCAOBS_TransmitterData_arraylength", c_ulong),
                ("clMyRTCAOBS_TransmitterData", RTCAOBS_clMyRTCAOBS_TransmitterData*72),
                ]


# noinspection PyTypeChecker
class GPSEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyEphemerisData_ulMySatelliteID", c_ulong),
                ("clMyEphemerisData_dMyTOW", c_double),
                ("clMyEphemerisData_ulMyHealth6", c_ulong),
                ("clMyEphemerisData_ulMyIODE1", c_ulong),
                ("clMyEphemerisData_ulMyIODE2", c_ulong),
                ("clMyEphemerisData_ulMyWN", c_ulong),
                ("clMyEphemerisData_ulMyZWN", c_ulong),
                ("clMyEphemerisData_dMyTOE", c_double),
                ("clMyEphemerisData_dMyA", c_double),
                ("clMyEphemerisData_dMyDeltaN", c_double),
                ("clMyEphemerisData_dMyM0", c_double),
                ("clMyEphemerisData_dMyEcc", c_double),
                ("clMyEphemerisData_dMyOmega", c_double),
                ("clMyEphemerisData_dMyCuc", c_double),
                ("clMyEphemerisData_dMyCus", c_double),
                ("clMyEphemerisData_dMyCrc", c_double),
                ("clMyEphemerisData_dMyCrs", c_double),
                ("clMyEphemerisData_dMyCic", c_double),
                ("clMyEphemerisData_dMyCis", c_double),
                ("clMyEphemerisData_dMyI0", c_double),
                ("clMyEphemerisData_dMyIDot", c_double),
                ("clMyEphemerisData_dMyOmega0", c_double),
                ("clMyEphemerisData_dMyOmegaDot", c_double),
                ("clMyEphemerisData_ulMyIODC", c_ulong),
                ("clMyEphemerisData_dMyTOC", c_double),
                ("clMyEphemerisData_dMyTGD", c_double),
                ("clMyEphemerisData_dMyAf0", c_double),
                ("clMyEphemerisData_dMyAf1", c_double),
                ("clMyEphemerisData_dMyAf2", c_double),
                ("clMyEphemerisData_bMyAntiSpoofing", c_bool),
                ("clMyEphemerisData_dMyN", c_double),
                ("clMyEphemerisData_dMyEphVar", c_double),
                ]


# noinspection PyTypeChecker
class IONUTC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyIon_dMyA0", c_double),
                ("clMyIon_dMyA1", c_double),
                ("clMyIon_dMyA2", c_double),
                ("clMyIon_dMyA3", c_double),
                ("clMyIon_dMyB0", c_double),
                ("clMyIon_dMyB1", c_double),
                ("clMyIon_dMyB2", c_double),
                ("clMyIon_dMyB3", c_double),
                ("clMyUTC_ulMyWNt", c_ulong),
                ("clMyUTC_ulMyTot", c_ulong),
                ("clMyUTC_dMyA0", c_double),
                ("clMyUTC_dMyA1", c_double),
                ("clMyUTC_ulMyWNlsf", c_ulong),
                ("clMyUTC_ulMyDN", c_ulong),
                ("clMyUTC_lMyDeltaTls", c_long),
                ("clMyUTC_lMyDeltaTlsf", c_long),
                ("clMyUTC_ulMyDeltaTUTC", c_ulong),
                ]


# noinspection PyTypeChecker
class OBSERVATIONS_clMyObsBase_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySvPrn", c_ushort),
                ("usMySvFreq", c_ushort),
                ("dMyPsr", c_double),
                ("fMyVPsr", c_float),
                ("dMyAdr", c_double),
                ("fMyVAdr", c_float),
                ("fMyDop", c_float),
                ("fMyCNo", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ("dMyDIon", c_double),
                ("dMyVDIon", c_double),
                ("fMyDAcc", c_float),
                ("dMyVOpn", c_double),
                ("fMy1SecCodeErrorMeters", c_float),
                ("fMyDLLBandWidth", c_float),
                ("fMyVDop", c_float),
                ("eMyFreq", c_uint),
                ("ulMyState6ID", c_ulong),
                ("sigMyChan", c_int),
                ("fMyUserCNo", c_float),
                ]


# noinspection PyTypeChecker
class OBSERVATIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyObsBase_ulMyWN", c_ulong),
                ("clMyObsBase_dMyRecTime", c_double),
                ("clMyObsBase_aclMyObs_arraylength", c_ulong),
                ("clMyObsBase_aclMyObs", OBSERVATIONS_clMyObsBase_aclMyObs*325),
                ]


# noinspection PyTypeChecker
class RTCA1_clMyRTCAData_Corrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("PseudorangeCorrection", c_double),
                ("IssueofData", c_char),
                ("RangeRateCorrection", c_double),
                ("UDRE", c_float),
                ]


# noinspection PyTypeChecker
class RTCA1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAData_ModifiedZCount", c_double),
                ("clMyRTCAData_AEB", c_char),
                ("clMyRTCAData_Corrections_arraylength", c_ulong),
                ("clMyRTCAData_Corrections", RTCA1_clMyRTCAData_Corrections*72),
                ]


# noinspection PyTypeChecker
class RTCAREF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAREF_ucMyNovAtelDesignator", c_char),
                ("clMyRTCAREF_ucMySubTypeIndicator", c_char),
                ("clMyRTCAREF_dMyX", c_double),
                ("clMyRTCAREF_dMyY", c_double),
                ("clMyRTCAREF_dMyZ", c_double),
                ("clMyRTCAREF_Reserved", c_char),
                ]


# noinspection PyTypeChecker
class CLOCKMODEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("ulMyRejectCount", c_ulong),
                ("clMyNoiseTime_ulMyMilliseconds", c_ulong),
                ("clMyUpdateTime_ulMyMilliseconds", c_ulong),
                ("adMyPar", c_double*3),
                ("clMyCov_adMyData", c_double*9),
                ("dMyInstRangeBias", c_double),
                ("dMyInstDrift", c_double),
                ("bMyConstellationChange", c_bool),
                ]


# noinspection PyTypeChecker
class DECODERCMDS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySignalChannelNumber", c_ulong),
                ("ulMyPrn", c_ulong),
                ("eMyCommandRequest", c_uint),
                ("eMyNavMssgDataType", c_uint),
                ("uiMyMaxNumberOfParityFailures", c_uint),
                ]


# noinspection PyTypeChecker
class RAWNAVDATA_aclMyRawNavData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("cMyDataBit", c_char),
                ("ucMyPowerStatus", c_char),
                ("ulMyResetLockCount", c_ulong),
                ]


# noinspection PyTypeChecker
class RAWNAVDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChan", c_ulong),
                ("ulMySatID", c_ulong),
                ("eMySignalType", c_uint),
                ("bMyNewData", c_bool),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyRawNavData_arraylength", c_ulong),
                ("aclMyRawNavData", RAWNAVDATA_aclMyRawNavData*256),
                ]


# noinspection PyTypeChecker
class RAWGPSSUBFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iMyFrameDecoderNumber", c_int),
                ("ulMySatelliteID", c_ulong),
                ("clMyRawSubframeData_ulMySubFrameID", c_ulong),
                ("clMyRawSubframeData_aucMyRawSubFrameData", c_char*30),
                ("ulMySignalChannelNumber", c_ulong),
                ]


# noinspection PyTypeChecker
class CLOCKSTEERING(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySteeringSource", c_uint),
                ("eMySteeringState", c_uint),
                ("ulMyModulus", c_ulong),
                ("dMyEffectivePulseWidth", c_double),
                ("dMyBandwidth", c_double),
                ("fMySlope", c_float),
                ("dMyLastOffset", c_double),
                ("dMyLastRate", c_double),
                ]


# noinspection PyTypeChecker
class GPSOL_CTS_ChanStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usPrn", c_ushort),
                ("usFreq", c_ushort),
                ("ulChannelStatus", c_ulong),
                ("dPsr", c_double),
                ("fDoppler", c_float),
                ("fCNo", c_float),
                ("fLockTime", c_float),
                ("fMyPSRResidual", c_float),
                ("eMyPSRRangeReject", c_uint),
                ("fMyPSRFilterWeighting", c_float),
                ("fMyRTKResidual", c_float),
                ("eMyRTKAmbiguity", c_uint),
                ("fMyRTKFilterWeighting", c_float),
                ("bMyIsAzElAvail", c_bool),
                ("fMyAzimuth", c_float),
                ("fMyElevation", c_float),
                ]


# noinspection PyTypeChecker
class GPSOL_CTS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ePositionStatus", c_uint),
                ("eMyPositionType", c_uint),
                ("fMyTrackingElevationCutoff", c_float),
                ("fMyRTKElevationCutoff", c_float),
                ("ChanStatus_arraylength", c_ulong),
                ("ChanStatus", GPSOL_CTS_ChanStatus*325),
                ]


# noinspection PyTypeChecker
class CHANDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulChanTrackingStatus", c_ulong),
                ("usPrn", c_ushort),
                ("usFreq", c_ushort),
                ("eDataFormat", c_uint),
                ("acData_Len", c_ulong),
                ("acData", c_char*1024),
                ]


# noinspection PyTypeChecker
class GPSOL_MON(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iRow", c_int),
                ("iColumn", c_int),
                ("iColor", c_int),
                ("eScreenCode", c_uint),
                ("asMessage", c_char*256),
                ]


# noinspection PyTypeChecker
class GPSOL_POS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyLLH_clMyPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("dDouble", c_double),
                ("dDouble", c_double),
                ("dDouble", c_double),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("iInt", c_int),
                ("iInt", c_int),
                ("dDouble", c_double),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("iInt", c_int),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("iInt", c_int),
                ]


# noinspection PyTypeChecker
class VERSION_aclVersions(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eComponentType", c_uint),
                ("szModelName", c_char*16),
                ("szPSN", c_char*16),
                ("szHardwareVersion", c_char*16),
                ("szSoftwareVersion", c_char*16),
                ("szBootVersion", c_char*16),
                ("szCompileDate", c_char*12),
                ("szCompileTime", c_char*12),
                ]


# noinspection PyTypeChecker
class VERSION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclVersions_arraylength", c_ulong),
                ("aclVersions", VERSION_aclVersions*20),
                ]


# noinspection PyTypeChecker
class DEBUGMEMORY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMemoryTestResult", c_uint),
                ("ulMemoryBlock", c_ulong),
                ("ulMemoryHighWater", c_ulong),
                ("ulMaxMemory", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGPROCESS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eStackStatus", c_uint),
                ("ulStackPointer", c_ulong),
                ("ulStackSize", c_ulong),
                ("ulStackUsed", c_ulong),
                ("ulMemoryInUse", c_ulong),
                ("ulProgramCounter", c_ulong),
                ("dProfile", c_double),
                ("ulNumMsgQs", c_ulong),
                ("ulNumMsgsPending", c_ulong),
                ("ulNumRequestors", c_ulong),
                ("ulProcessID", c_ulong),
                ("szProcessName", c_char*100),
                ]


# noinspection PyTypeChecker
class RAWEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyWeek", c_ulong),
                ("ulMyTOE", c_ulong),
                ("clMyRawEphemerisData_aucMySubframe1", c_char*30),
                ("clMyRawEphemerisData_aucMySubframe2", c_char*30),
                ("clMyRawEphemerisData_aucMySubframe3", c_char*30),
                ]


# noinspection PyTypeChecker
class BESTPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class RANGE_clMyObsBase_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySvPrn", c_ushort),
                ("usMySvFreq", c_ushort),
                ("dMyPsr", c_double),
                ("fMySDPsr", c_float),
                ("dMyAdr", c_double),
                ("fMySDAdr", c_float),
                ("fMyDop", c_float),
                ("fMyUserCNo", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class RANGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyObsBase_aclMyObs_arraylength", c_ulong),
                ("clMyObsBase_aclMyObs", RANGE_clMyObsBase_aclMyObs*325),
                ]


# noinspection PyTypeChecker
class DECODERSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("bMyParityFailed", c_bool),
                ("bMyBitsFlipped", c_bool),
                ("bMyParityKnown", c_bool),
                ("ulMyResetLockCount", c_ulong),
                ("clMyTime_ulMyWeeks", c_ulong),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class PSRPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class SATVIS_aclMySatVisList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPrn", c_ushort),
                ("usMyFreq", c_ushort),
                ("ulMySatHealth", c_ulong),
                ("dMyElevation", c_double),
                ("dMyAzimuth", c_double),
                ("dMyTrueDoppler", c_double),
                ("dMyApparentDoppler", c_double),
                ]


# noinspection PyTypeChecker
class SATVIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("bMyIsSatVisValid", c_bool),
                ("bMyWasGPSAlmanacUsed", c_bool),
                ("aclMySatVisList_arraylength", c_ulong),
                ("aclMySatVisList", SATVIS_aclMySatVisList*318),
                ]


# noinspection PyTypeChecker
class BAT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("Source", c_uint),
                ("BattA", c_int),
                ("BattB", c_int),
                ]


# noinspection PyTypeChecker
class PROPAGATEDCLOCKMODEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyRangeBias", c_double),
                ("dMyDrift", c_double),
                ("dMyRangeBiasVariance", c_double),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class PORTSTATS_aclMyPortStatistics(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("ulMyRXChars", c_ulong),
                ("ulMyTXChars", c_ulong),
                ("ulMyGoodRXChars", c_ulong),
                ("ulMyDroppedChars", c_ulong),
                ("ulMyInterrupts", c_ulong),
                ("ulMyBreaks", c_ulong),
                ("ulMyParityErrors", c_ulong),
                ("ulMyFramingErrors", c_ulong),
                ("ulMyOverRuns", c_ulong),
                ]


# noinspection PyTypeChecker
class PORTSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyPortStatistics_arraylength", c_ulong),
                ("aclMyPortStatistics", PORTSTATS_aclMyPortStatistics*33),
                ]


# noinspection PyTypeChecker
class ALMANAC_aclMySVAlmData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulPRN", c_ulong),
                ("ulMyWn", c_ulong),
                ("dMyTOA", c_double),
                ("dMyEcc", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmega", c_double),
                ("dMyMo", c_double),
                ("dMyAf0", c_double),
                ("dMyAf1", c_double),
                ("dMyN", c_double),
                ("dMyA", c_double),
                ("dMyDi", c_double),
                ("ulMySvConfiguration", c_ulong),
                ("ulMyHealth6", c_ulong),
                ("ulMyHealth8", c_ulong),
                ("bMyAntiSpoofingSet", c_bool),
                ]


# noinspection PyTypeChecker
class ALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySVAlmData_arraylength", c_ulong),
                ("aclMySVAlmData", ALMANAC_aclMySVAlmData*32),
                ]


# noinspection PyTypeChecker
class RAWALM_aclMySubFramePages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usSVID", c_ushort),
                ("aucMyPageRawData", c_char*30),
                ]


# noinspection PyTypeChecker
class RAWALM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyTOA_ulMyWeeks", c_ulong),
                ("clMyTOA_ulMyMilliseconds", c_ulong),
                ("aclMySubFramePages_arraylength", c_ulong),
                ("aclMySubFramePages", RAWALM_aclMySubFramePages*46),
                ]


# noinspection PyTypeChecker
class GPSOL_VEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("ulULONG", c_ulong),
                ("clMyVelocity_clMyCommonSolution_dMySpeed", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("dDouble", c_double),
                ("dDouble", c_double),
                ("dDouble", c_double),
                ]


# noinspection PyTypeChecker
class RTCAOBSIN_clMyRTCAOBS_TransmitterData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("L1LockFlag", c_char),
                ("L2LockFlag", c_char),
                ("L1PseudorangeOffset", c_double),
                ("L2PseudorangeOffset", c_double),
                ("L1ADROffset", c_float),
                ("L2ADROffset", c_float),
                ("L2NotEncrypted", c_bool),
                ("Reserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCAOBSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clHeader_clMyRTCAOBS_ulMessageIdentifier", c_ulong),
                ("clHeader_clMyRTCAOBS_ulRefStation", c_ulong),
                ("clHeader_clMyRTCAOBS_ulMessageType", c_ulong),
                ("clHeader_clMyRTCAOBS_ulReserved", c_ulong),
                ("clHeader_clMyRTCAOBS_ulMessageLength", c_ulong),
                ("clMyRTCAOBS_NovAtelDesignator", c_char),
                ("clMyRTCAOBS_SubtypeIndicator", c_char),
                ("clMyRTCAOBS_MinimumPseudorange", c_double),
                ("clMyRTCAOBS_Seconds", c_float),
                ("clMyRTCAOBS_Reserved", c_int),
                ("clMyRTCAOBS_TransmitterData_arraylength", c_ulong),
                ("clMyRTCAOBS_TransmitterData", RTCAOBSIN_clMyRTCAOBS_TransmitterData*72),
                ]


# noinspection PyTypeChecker
class RTCAREFIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCAREF_ulMessageIdentifier", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulRefStation", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulMessageType", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulReserved", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulMessageLength", c_ulong),
                ("clMyRTCAREF_ucMyNovAtelDesignator", c_char),
                ("clMyRTCAREF_ucMySubTypeIndicator", c_char),
                ("clMyRTCAREF_dMyX", c_double),
                ("clMyRTCAREF_dMyY", c_double),
                ("clMyRTCAREF_dMyZ", c_double),
                ("clMyRTCAREF_Reserved", c_char),
                ]


# noinspection PyTypeChecker
class GPSOL_AZEL_aclMySatelliteStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPrn", c_ushort),
                ("usMyFreq", c_ushort),
                ("bMyHasPrimary", c_bool),
                ("bMyHasSecondary", c_bool),
                ("ulMyPrimaryTrackingStatus", c_ulong),
                ("ulMySecondaryTrackingStatus", c_ulong),
                ("dMyPrimaryPsr", c_double),
                ("dMySecondaryPsr", c_double),
                ("fMyPrimaryDoppler", c_float),
                ("fMySecondaryDoppler", c_float),
                ("fMyPrimaryCNo", c_float),
                ("fMySecondaryCNo", c_float),
                ("fMyPrimaryLockTime", c_float),
                ("fMySecondaryLockTime", c_float),
                ("fMyPrimaryPSRResidual", c_float),
                ("fMySecondaryPSRResidual", c_float),
                ("eMyPrimaryRangeReject", c_uint),
                ("eMySecondaryRangeReject", c_uint),
                ("fMyPrimaryPSRFWgt", c_float),
                ("fMySecondaryPSRFWgt", c_float),
                ("fMyPrimaryRTKResid", c_float),
                ("fMySecondaryRTKResid", c_float),
                ("eMyPrimaryRTKAmb", c_uint),
                ("eMySecondaryRTKAmb", c_uint),
                ("fMyPrimaryRTKFWgt", c_float),
                ("fMySecondaryRTKFWgt", c_float),
                ("bMyIsAzElAvail", c_bool),
                ("fMyAzimuth", c_float),
                ("fMyElevation", c_float),
                ]


# noinspection PyTypeChecker
class GPSOL_AZEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPositionStatus", c_uint),
                ("eMyPositionType", c_uint),
                ("fMyTrackingElevationCutoff", c_float),
                ("fMyRTKElevationCutoff", c_float),
                ("fMyGDOP", c_float),
                ("fMyPDOP", c_float),
                ("fMyHDOP", c_float),
                ("fMyTDOP", c_float),
                ("aclMySatelliteStatus_arraylength", c_ulong),
                ("aclMySatelliteStatus", GPSOL_AZEL_aclMySatelliteStatus*50),
                ]


# noinspection PyTypeChecker
class TRACKSTAT_ChanStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usPrn", c_ushort),
                ("usFreq", c_ushort),
                ("ulChannelStatus", c_ulong),
                ("dPsr", c_double),
                ("fDoppler", c_float),
                ("fCNo", c_float),
                ("fLockTime", c_float),
                ("fMyPSRResidual", c_float),
                ("eMyPSRRangeReject", c_uint),
                ("fMyPSRFilterWeighting", c_float),
                ]


# noinspection PyTypeChecker
class TRACKSTAT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ePositionStatus", c_uint),
                ("eMyPositionType", c_uint),
                ("fMyTrackingElevationCutoff", c_float),
                ("ChanStatus_arraylength", c_ulong),
                ("ChanStatus", TRACKSTAT_ChanStatus*325),
                ]


# noinspection PyTypeChecker
class SATSTAT_aclMySatelliteStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPrn", c_ushort),
                ("usMyFreq", c_ushort),
                ("bMyHasPrimary", c_bool),
                ("bMyHasSecondary", c_bool),
                ("ulMyPrimaryTrackingStatus", c_ulong),
                ("ulMySecondaryTrackingStatus", c_ulong),
                ("dMyPrimaryPsr", c_double),
                ("dMySecondaryPsr", c_double),
                ("fMyPrimaryDoppler", c_float),
                ("fMySecondaryDoppler", c_float),
                ("fMyPrimaryCNo", c_float),
                ("fMySecondaryCNo", c_float),
                ("fMyPrimaryLockTime", c_float),
                ("fMySecondaryLockTime", c_float),
                ("fMyPrimaryPSRResidual", c_float),
                ("fMySecondaryPSRResidual", c_float),
                ("eMyPrimaryRangeReject", c_uint),
                ("eMySecondaryRangeReject", c_uint),
                ("fMyPrimaryPSRFWgt", c_float),
                ("fMySecondaryPSRFWgt", c_float),
                ("fMyPrimaryRTKResid", c_float),
                ("fMySecondaryRTKResid", c_float),
                ("eMyPrimaryRTKAmb", c_uint),
                ("eMySecondaryRTKAmb", c_uint),
                ("fMyPrimaryRTKFWgt", c_float),
                ("fMySecondaryRTKFWgt", c_float),
                ("bMyIsAzElAvail", c_bool),
                ("fMyAzimuth", c_float),
                ("fMyElevation", c_float),
                ]


# noinspection PyTypeChecker
class SATSTAT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPositionStatus", c_uint),
                ("eMyPositionType", c_uint),
                ("fMyTrackingElevationCutoff", c_float),
                ("fMyRTKElevationCutoff", c_float),
                ("aclMySatelliteStatus_arraylength", c_ulong),
                ("aclMySatelliteStatus", SATSTAT_aclMySatelliteStatus*50),
                ("fMyGDOP", c_float),
                ("fMyPDOP", c_float),
                ("fMyHDOP", c_float),
                ("fMyTDOP", c_float),
                ]


# noinspection PyTypeChecker
class LOOPACCUM_aclMyChannelLoopAccum(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyAccumPeriodMS", c_ulong),
                ("ulMyIQAccumTimeUS", c_ulong),
                ("ulMyCarrierAccumTimeUS", c_ulong),
                ("ulMyCodeAccumTimeUS", c_ulong),
                ]


# noinspection PyTypeChecker
class LOOPACCUM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyChannelLoopAccum_arraylength", c_ulong),
                ("aclMyChannelLoopAccum", LOOPACCUM_aclMyChannelLoopAccum*325),
                ]


# noinspection PyTypeChecker
class LOOPGAINS_aclMyChannelLoopGains(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyPhaseBand", c_float),
                ("fMyPhaseGain", c_float),
                ("fMyPhaseRateGain", c_float),
                ("fMyPhaseAccGain", c_float),
                ("fMyCodeBand", c_float),
                ("fMyCodeGain", c_float),
                ("fMyCodeRateGain", c_float),
                ]


# noinspection PyTypeChecker
class LOOPGAINS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyChannelLoopGains_arraylength", c_ulong),
                ("aclMyChannelLoopGains", LOOPGAINS_aclMyChannelLoopGains*325),
                ]


# noinspection PyTypeChecker
class RXSTATUS_aclMyStatusWords(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStatusWord", c_ulong),
                ("ulMyPriorityMask", c_ulong),
                ("ulMyEventSetMask", c_ulong),
                ("ulMyEventClearMask", c_ulong),
                ]


# noinspection PyTypeChecker
class RXSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyRxError", c_ulong),
                ("aclMyStatusWords_arraylength", c_ulong),
                ("aclMyStatusWords", RXSTATUS_aclMyStatusWords*5),
                ]


# noinspection PyTypeChecker
class RXSTATUSEVENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyWord", c_uint),
                ("ulMyBitPosition", c_ulong),
                ("eMyEvent", c_uint),
                ("szDescription", c_char*32),
                ]


# noinspection PyTypeChecker
class MATCHEDPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class BESTVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("eMyType", c_uint),
                ("clMyVelocity_fMyLatency", c_float),
                ("fMyDifferentialLag", c_float),
                ("clMyVelocity_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_dMyZ", c_double),
                ("lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class PSRVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class TIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eClockModelStatus", c_uint),
                ("dOffset", c_double),
                ("dOffsetStd", c_double),
                ("dUTCOffset", c_double),
                ("ulUTCYear", c_ulong),
                ("ucUTCMonth", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCHour", c_char),
                ("ucUTCMinute", c_char),
                ("ulUTCMillisecond", c_ulong),
                ("UTCTimeStatus", c_uint),
                ]


# noinspection PyTypeChecker
class CMROBS_clMyType0Message_aclMyCMRBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySlotNumber", c_ulong),
                ("bMyCodeFlag", c_bool),
                ("bMyL1PhaseValid", c_bool),
                ("bMyIsL2Present", c_bool),
                ("ulMyL1Psr", c_ulong),
                ("lMyL1CarrierOffset", c_long),
                ("ulMyL1Snr", c_ulong),
                ("ulMyL1SlipCount", c_ulong),
                ("bMyIsL2Code", c_bool),
                ("bMyCodeType", c_bool),
                ("bMyIsL2CodeValid", c_bool),
                ("bMyIsL2PhaseValid", c_bool),
                ("bMyPhaseFull", c_bool),
                ("ulMyReserved", c_ulong),
                ("lMyL2RangeOffset", c_long),
                ("lMyL2CarrierOffset", c_long),
                ("ulMyL2Snr", c_ulong),
                ("ulMyL2SlipCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CMROBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyType0Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyType0Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyType0Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyType0Message_ulMyLength", c_ulong),
                ("clMyType0Message_ulMyVersion", c_ulong),
                ("clMyType0Message_ulMyStationID", c_ulong),
                ("clMyType0Message_ulMessageType", c_ulong),
                ("clMyType0Message_ulMyNumberofSv", c_ulong),
                ("clMyType0Message_ulMyEpochTime", c_ulong),
                ("clMyType0Message_ulMyClockBiasValid", c_ulong),
                ("clMyType0Message_lMyClockOffset", c_long),
                ("clMyType0Message_aclMyCMRBody_arraylength", c_ulong),
                ("clMyType0Message_aclMyCMRBody", CMROBS_clMyType0Message_aclMyCMRBody*24),
                ]


# noinspection PyTypeChecker
class CMROBSIN_clMyCMROBS_aclMyCMRBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySlotNumber", c_ulong),
                ("bMyCodeFlag", c_bool),
                ("bMyL1PhaseValid", c_bool),
                ("bMyIsL2Present", c_bool),
                ("ulMyL1Psr", c_ulong),
                ("lMyL1CarrierOffset", c_long),
                ("ulMyL1Snr", c_ulong),
                ("ulMyL1SlipCount", c_ulong),
                ("bMyIsL2Code", c_bool),
                ("bMyCodeType", c_bool),
                ("bMyIsL2CodeValid", c_bool),
                ("bMyIsL2PhaseValid", c_bool),
                ("bMyPhaseFull", c_bool),
                ("ulMyReserved", c_ulong),
                ("lMyL2RangeOffset", c_long),
                ("lMyL2CarrierOffset", c_long),
                ("ulMyL2Snr", c_ulong),
                ("ulMyL2SlipCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CMROBSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyCMROBS_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyCMROBS_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyCMROBS_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyCMROBS_ulMyLength", c_ulong),
                ("clMyCMROBS_ulMyVersion", c_ulong),
                ("clMyCMROBS_ulMyStationID", c_ulong),
                ("clMyCMROBS_ulMessageType", c_ulong),
                ("clMyCMROBS_ulMyNumberofSv", c_ulong),
                ("clMyCMROBS_ulMyEpochTime", c_ulong),
                ("clMyCMROBS_ulMyClockBiasValid", c_ulong),
                ("clMyCMROBS_lMyClockOffset", c_long),
                ("clMyCMROBS_aclMyCMRBody_arraylength", c_ulong),
                ("clMyCMROBS_aclMyCMRBody", CMROBSIN_clMyCMROBS_aclMyCMRBody*24),
                ]


# noinspection PyTypeChecker
class CMRREF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clType1Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clType1Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clType1Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clType1Message_ulMyLength", c_ulong),
                ("clType1Message_ulMyVersion", c_ulong),
                ("clType1Message_ulMyStationID", c_ulong),
                ("clType1Message_ulMyMessageType", c_ulong),
                ("clType1Message_bMyIsBatteryLow", c_bool),
                ("clType1Message_bMyIsMemLow", c_bool),
                ("clType1Message_ulMyReserved", c_ulong),
                ("clType1Message_bMyIsL2Enabled", c_bool),
                ("clType1Message_ulMyReserved2", c_ulong),
                ("clType1Message_ulMyEpochTime", c_ulong),
                ("clType1Message_ulMyMotionState", c_ulong),
                ("clType1Message_ulMyAntennaNumber", c_ulong),
                ("clMyCMRBody_clType1Message_dMyECEF_X", c_double),
                ("clMyCMRBody_clType1Message_ulMyAntennaH", c_ulong),
                ("clMyCMRBody_clType1Message_dMyECEF_Y", c_double),
                ("clMyCMRBody_clType1Message_ulMyEastOffset", c_ulong),
                ("clMyCMRBody_clType1Message_dMyECEF_Z", c_double),
                ("clMyCMRBody_clType1Message_ulMyNorthOffset", c_ulong),
                ("clMyCMRBody_clType1Message_ulMyPosAccuracy", c_ulong),
                ("clMyCMRBody_clType1Message_ulMyReserved", c_ulong),
                ]


# noinspection PyTypeChecker
class CMRREFIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyType1Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyType1Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyType1Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyType1Message_ulMyLength", c_ulong),
                ("clMyType1Message_ulMyVersion", c_ulong),
                ("clMyType1Message_ulMyStationID", c_ulong),
                ("clMyType1Message_ulMyMessageType", c_ulong),
                ("clMyType1Message_bMyIsBatteryLow", c_bool),
                ("clMyType1Message_bMyIsMemLow", c_bool),
                ("clMyType1Message_ulMyReserved", c_ulong),
                ("clMyType1Message_bMyIsL2Enabled", c_bool),
                ("clMyType1Message_ulMyReserved2", c_ulong),
                ("clMyType1Message_ulMyEpochTime", c_ulong),
                ("clMyType1Message_ulMyMotionState", c_ulong),
                ("clMyType1Message_ulMyAntennaNumber", c_ulong),
                ("clMyCMRBody_clMyType1Message_dMyECEF_X", c_double),
                ("clMyCMRBody_clMyType1Message_ulMyAntennaH", c_ulong),
                ("clMyCMRBody_clMyType1Message_dMyECEF_Y", c_double),
                ("clMyCMRBody_clMyType1Message_ulMyEastOffset", c_ulong),
                ("clMyCMRBody_clMyType1Message_dMyECEF_Z", c_double),
                ("clMyCMRBody_clMyType1Message_ulMyNorthOffset", c_ulong),
                ("clMyCMRBody_clMyType1Message_ulMyPosAccuracy", c_ulong),
                ("clMyCMRBody_clMyType1Message_ulMyReserved", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM1_clMyRTCM1_9_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM1_9_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMyHealth", c_ulong),
                ("clMyRTCM1_9_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM1_9_aclMyDiffData", RTCM1_clMyRTCM1_9_aclMyDiffData*325),
                ]


# noinspection PyTypeChecker
class RTCM18OUT_clMyRTCM18_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("lMyAdr", c_long),
                ]


# noinspection PyTypeChecker
class RTCM18OUT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM18_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyHealth", c_ulong),
                ("clMyRTCM18_ulMyFreq", c_ulong),
                ("clMyRTCM18_ulMySpare", c_ulong),
                ("clMyRTCM18_lMyTime", c_long),
                ("clMyRTCM18_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM18_aclMyRTCMBody", RTCM18OUT_clMyRTCM18_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCM19OUT_clMyRTCM19_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyPsr", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM19OUT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM19_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyHealth", c_ulong),
                ("clMyRTCM19_ulMyFreq", c_ulong),
                ("clMyRTCM19_ulMySmoothingInterval", c_ulong),
                ("clMyRTCM19_lMyTime", c_long),
                ("clMyRTCM19_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM19_aclMyRTCMBody", RTCM19OUT_clMyRTCM19_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCM1IN_clMyRTCM_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM1IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyHealth", c_ulong),
                ("clMyRTCM_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM_aclMyDiffData", RTCM1IN_clMyRTCM_aclMyDiffData*325),
                ]


# noinspection PyTypeChecker
class RTCM20IN_clMyRTCMOBS_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("ulIODE", c_ulong),
                ("lPhaseCorr", c_long),
                ]


# noinspection PyTypeChecker
class RTCM20IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyHealth", c_ulong),
                ("clMyRTCMOBS_ulMyFreq", c_ulong),
                ("clMyRTCMOBS_ulSpare", c_ulong),
                ("clMyRTCMOBS_lMyTime", c_long),
                ("clMyRTCMOBS_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCMOBS_aclMyRTCMBody", RTCM20IN_clMyRTCMOBS_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCM21IN_clMyRTCMOBS_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyRateCorrSF", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyPsrCorrSF", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyIODE", c_ulong),
                ("lMyPsrCorr", c_long),
                ("lMyPsrCorrRate", c_long),
                ]


# noinspection PyTypeChecker
class RTCM21IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyHealth", c_ulong),
                ("clMyRTCMOBS_ulMyFreq", c_ulong),
                ("clMyRTCMOBS_ulMySmoothingInterval", c_ulong),
                ("clMyRTCMOBS_lMyTime", c_long),
                ("clMyRTCMOBS_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCMOBS_aclMyRTCMBody", RTCM21IN_clMyRTCMOBS_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCM22IN_clMyRTCMBody_clMyRTCMREF_clMyRTCM22AntHgtL1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulSpareBits", c_ulong),
                ("ulMyConstellation", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM22IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMREF_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCMREF_lMyL1AntDeltaX", c_long),
                ("clMyRTCMBody_clMyRTCMREF_lMyL1AntDeltaY", c_long),
                ("clMyRTCMBody_clMyRTCMREF_lMyL1AntDeltaZ", c_long),
                ("clMyRTCMBody_clMyRTCMREF_clMyRTCM22AntHgtL1_arraylength", c_ulong),
                ("clMyRTCMBody_clMyRTCMREF_clMyRTCM22AntHgtL1", RTCM22IN_clMyRTCMBody_clMyRTCMREF_clMyRTCM22AntHgtL1*1),
                ]


# noinspection PyTypeChecker
class RTCM3IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMREF_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_Z", c_double),
                ]


# noinspection PyTypeChecker
class RTCM59IN_clMyRTCM59_clMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySv", c_ulong),
                ("ulMyLock", c_ulong),
                ("ulMyPsr", c_ulong),
                ("lMyAdrCor", c_long),
                ]


# noinspection PyTypeChecker
class RTCM59IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM59_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59_ulMyHealth", c_ulong),
                ("clMyRTCM59_ucMySubType", c_char),
                ("clMyRTCM59_lMyMinPsr", c_long),
                ("clMyRTCM59_lTimeOffset", c_long),
                ("clMyRTCM59_ulSpareBits", c_ulong),
                ("clMyRTCM59_clMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM59_clMyRTCMBody", RTCM59IN_clMyRTCM59_clMyRTCMBody*325),
                ]


# noinspection PyTypeChecker
class RTCM59_clRTCM59_clMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySv", c_ulong),
                ("ulMyLock", c_ulong),
                ("ulMyPsr", c_ulong),
                ("lMyAdrCor", c_long),
                ]


# noinspection PyTypeChecker
class RTCM59(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clRTCM59_ulMyType", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulRefID", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMyHealth", c_ulong),
                ("clRTCM59_ucMySubType", c_char),
                ("clRTCM59_lMyMinPsr", c_long),
                ("clRTCM59_lTimeOffset", c_long),
                ("clRTCM59_ulSpareBits", c_ulong),
                ("clRTCM59_clMyRTCMBody_arraylength", c_ulong),
                ("clRTCM59_clMyRTCMBody", RTCM59_clRTCM59_clMyRTCMBody*325),
                ]


# noinspection PyTypeChecker
class RTCM3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM3_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM3_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCM3_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCM3_dMyECEF_Z", c_double),
                ]


# noinspection PyTypeChecker
class RTCM22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulSpareBits", c_ulong),
                ("ulMyConstellation", c_ulong),
                ("ulMyAntennaType", c_ulong),
                ("ulMyAntennaRefPoint", c_ulong),
                ("bNoHeight", c_bool),
                ("ulAntennaPhaseHeight", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyL2AntDeltaX", c_long),
                ("lMyL2AntDeltaY", c_long),
                ("lMyL2AntDeltaZ", c_long),
                ]


# noinspection PyTypeChecker
class RTCM22(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM22_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaX", c_long),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaY", c_long),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaZ", c_long),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1_arraylength", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1", RTCM22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1*1),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2_arraylength", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2", RTCM22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2*1),
                ]


# noinspection PyTypeChecker
class RTCM21OUT_clMyRTCM21_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyRateCorrSF", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyPsrCorrSF", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyIODE", c_ulong),
                ("lMyPsrCorr", c_long),
                ("lMyPsrCorrRate", c_long),
                ]


# noinspection PyTypeChecker
class RTCM21OUT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM21_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyHealth", c_ulong),
                ("clMyRTCM21_ulMyFreq", c_ulong),
                ("clMyRTCM21_ulMySmoothingInterval", c_ulong),
                ("clMyRTCM21_lMyTime", c_long),
                ("clMyRTCM21_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM21_aclMyRTCMBody", RTCM21OUT_clMyRTCM21_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCM20OUT_clMyRTCM20_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("ulIODE", c_ulong),
                ("lPhaseCorr", c_long),
                ]


# noinspection PyTypeChecker
class RTCM20OUT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM20_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyHealth", c_ulong),
                ("clMyRTCM20_ulMyFreq", c_ulong),
                ("clMyRTCM20_ulSpare", c_ulong),
                ("clMyRTCM20_lMyTime", c_long),
                ("clMyRTCM20_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM20_aclMyRTCMBody", RTCM20OUT_clMyRTCM20_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCM19IN_clMyRTCMOBS_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyPsr", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM19IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyHealth", c_ulong),
                ("clMyRTCMOBS_ulMyFreq", c_ulong),
                ("clMyRTCMOBS_ulMySmoothingInterval", c_ulong),
                ("clMyRTCMOBS_lMyTime", c_long),
                ("clMyRTCMOBS_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCMOBS_aclMyRTCMBody", RTCM19IN_clMyRTCMOBS_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCM18IN_clMyRTCMOBS_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("lMyAdr", c_long),
                ]


# noinspection PyTypeChecker
class RTCM18IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMOBS_ulMyHealth", c_ulong),
                ("clMyRTCMOBS_ulMyFreq", c_ulong),
                ("clMyRTCMOBS_ulMySpare", c_ulong),
                ("clMyRTCMOBS_lMyTime", c_long),
                ("clMyRTCMOBS_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCMOBS_aclMyRTCMBody", RTCM18IN_clMyRTCMOBS_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RANGEPN_clMyObsBase_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySvPrn", c_ushort),
                ("usMySvFreq", c_ushort),
                ("dMyPsr", c_double),
                ("fMySDPsr", c_float),
                ("dMyAdr", c_double),
                ("fMySDAdr", c_float),
                ("fMyDop", c_float),
                ("fMyUserCNo", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ("dMyVOpn", c_double),
                ]


# noinspection PyTypeChecker
class RANGEPN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fFloat", c_float),
                ("clMyObsBase_aclMyObs_arraylength", c_ulong),
                ("clMyObsBase_aclMyObs", RANGEPN_clMyObsBase_aclMyObs*325),
                ]


# noinspection PyTypeChecker
class RXCONFIG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ConfigCmdClass_MessageId", c_ulong),
                ("ConfigCmdClass_MessageLength", c_ulong),
                ("ConfigCmdClass_MessageBuffer", c_char*450),
                ]


# noinspection PyTypeChecker
class RTCM16(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM16_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM16_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM16_aucMyRTCM16Text_Len", c_ulong),
                ("clMyRTCMBody_clMyRTCM16_aucMyRTCM16Text", c_char*90),
                ]


# noinspection PyTypeChecker
class RTCM16IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM16_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM16_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM16_aucMyRTCM16Text_Len", c_ulong),
                ("clMyRTCMBody_clMyRTCM16_aucMyRTCM16Text", c_char*90),
                ]


# noinspection PyTypeChecker
class DEBUGETHERS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyEtherName", c_char*51),
                ("ulMyEtherNum", c_ulong),
                ("ulMyEtherSiblingNum", c_ulong),
                ("ulMyNumPackets", c_ulong),
                ("ulMyNumRequestors", c_ulong),
                ("bMyIsCommMsgQTaken", c_bool),
                ("ulMyCommMsgQID", c_ulong),
                ("ulMyProviderTaskID", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGMSGQS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyProcessID", c_ulong),
                ("ulMyQueueID", c_ulong),
                ("ulMyNumMsgs", c_ulong),
                ("ulMyMaxMsgs", c_ulong),
                ]


# noinspection PyTypeChecker
class RANGECMP_aclMyRangeCEntry(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucRangeCData", c_char*24),
                ]


# noinspection PyTypeChecker
class RANGECMP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyRangeCEntry_arraylength", c_ulong),
                ("aclMyRangeCEntry", RANGECMP_aclMyRangeCEntry*325),
                ]


# noinspection PyTypeChecker
class RTKPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class FILEDUMP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("PacketId", c_ulong),
                ("DataBytes_Len", c_ulong),
                ("DataBytes", c_char*1024),
                ]


# noinspection PyTypeChecker
class FILEHDR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("Name32769", c_char*12),
                ("FileSize", c_ulong),
                ("MinSats", c_ulong),
                ("StartWeek", c_ulong),
                ("StopWeek", c_ulong),
                ("StartSec", c_ulong),
                ("StopSec", c_ulong),
                ("Reserved1", c_int),
                ("Reserved2", c_double),
                ("Reserved3", c_ulong),
                ("Reserved4", c_ulong),
                ("FileStatus", c_ulong),
                ("VersionP", c_ulong),
                ("TimeP", c_ulong),
                ("ProjectP", c_ulong),
                ("GroupP", c_ulong),
                ("SiteP", c_ulong),
                ("MetP", c_ulong),
                ("WriteOutP", c_ulong),
                ("Reserved6", c_ulong),
                ("Reserved7", c_ulong),
                ("Reserved8", c_ulong),
                ("Reserved9", c_ulong),
                ]


# noinspection PyTypeChecker
class GROUPDEF_LogSpecs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("MessageId", c_ulong),
                ("Trigger", c_uint),
                ("Rate", c_float),
                ("PortChannel", c_uint),
                ("Reserved1", c_float),
                ("Reserved2", c_ushort),
                ("Reserved3", c_char),
                ("Reserved4", c_char),
                ]


# noinspection PyTypeChecker
class GROUPDEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("GroupName", c_char*12),
                ("SessionName", c_char*8),
                ("AntSN", c_char*16),
                ("AntType", c_char*16),
                ("AntHeight", c_float),
                ("Name32774", c_float),
                ("SatLimit", c_int),
                ("GroupStatus", c_ulong),
                ("GroupStatus2", c_ulong),
                ("LatTime", c_double),
                ("LongHorz", c_double),
                ("HeightVert", c_double),
                ("SiteNum", c_char*8),
                ("SiteName", c_char*32),
                ("DGPSTxIdType", c_uint),
                ("DGPSTxId", c_char*5),
                ("Reserved5", c_char),
                ("Reserved6", c_ushort),
                ("InterfaceModes", c_ulong),
                ("Reserved3", c_double),
                ("Reserved4", c_int),
                ("LogSpecs_arraylength", c_ulong),
                ("LogSpecs", GROUPDEF_LogSpecs*20),
                ]


# noinspection PyTypeChecker
class METDEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("MetP", c_ulong),
                ("MetStatus", c_ulong),
                ("Temp", c_float),
                ("Press", c_float),
                ("Humid", c_float),
                ]


# noinspection PyTypeChecker
class SCHDEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("Index", c_ulong),
                ("Group", c_char*12),
                ("StartTime", c_char*12),
                ("StopTime", c_char*12),
                ("FileName", c_char*12),
                ]


# noinspection PyTypeChecker
class SITEDEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SiteP", c_ulong),
                ("SiteNum", c_char*8),
                ("SiteName", c_char*32),
                ("Attrib", c_int),
                ("AntHeight", c_float),
                ("Name32774", c_char*16),
                ("FirstGPSWeek", c_ulong),
                ("LastGPSWeek", c_ulong),
                ("FirstGPSSec", c_ulong),
                ("LastGPSSec", c_ulong),
                ("SiteStatus", c_ulong),
                ("Reserved", c_ulong),
                ]


# noinspection PyTypeChecker
class PROJECTDEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("Project", c_char*32),
                ("Agency", c_char*32),
                ("Observer", c_char*32),
                ]


# noinspection PyTypeChecker
class FILECHANNEL_ChannelEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("PortChannel", c_uint),
                ("SatLimit", c_int),
                ("Reserved1", c_ulong),
                ("Reserved2", c_ulong),
                ("FileName", c_char*12),
                ]


# noinspection PyTypeChecker
class FILECHANNEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("DiskSpace", c_ulong),
                ("FlashCardModel", c_char*40),
                ("FlashVersion", c_char*8),
                ("Reserved1", c_ulong),
                ("Reserved2", c_char*16),
                ("ChannelEntries_arraylength", c_ulong),
                ("ChannelEntries", FILECHANNEL_ChannelEntries*32),
                ]


# noinspection PyTypeChecker
class DIRENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("FileName", c_char*128),
                ("SizeBytes", c_ulong),
                ("SizePackets", c_ulong),
                ("LastChangeDate", c_ulong),
                ("LastChangeTime", c_ulong),
                ]


# noinspection PyTypeChecker
class NAVIGATE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPositionStatus", c_uint),
                ("eMyPositionType", c_uint),
                ("eMyVelocityStatus", c_uint),
                ("eMyNavStatus", c_uint),
                ("dMyDistance", c_double),
                ("dMyBearing", c_double),
                ("dMyAlongTrack", c_double),
                ("dMyXTrack", c_double),
                ("ulMyETAWeeks", c_ulong),
                ("dMyETASeconds", c_double),
                ]


# noinspection PyTypeChecker
class AVEPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyWGS84LLH_dMyLatitude", c_double),
                ("clMyWGS84LLH_dMyLongitude", c_double),
                ("dMyMSLHeight", c_double),
                ("dMyWGS84StdDev_fMyLatStdDev", c_float),
                ("dMyWGS84StdDev_fMyLongStdDev", c_float),
                ("dMyWGS84StdDev_fMyHgtStdDev", c_float),
                ("eMyAveStatus", c_uint),
                ("ulMyAveTime", c_ulong),
                ("ulMyNumSample", c_ulong),
                ]


# noinspection PyTypeChecker
class PSRDOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyHTDOP", c_float),
                ("clMyDOPs_fMyTDOP", c_float),
                ("clMyDOPs_fMyGPSElevMask", c_float),
                ("clMyDOPs_aulMySats_Len", c_ulong),
                ("clMyDOPs_aulMySats", c_ulong*325),
                ]


# noinspection PyTypeChecker
class REFSTATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyRefStatus", c_ulong),
                ("dMyECEF_X", c_double),
                ("dMyECEF_Y", c_double),
                ("dMyECEF_Z", c_double),
                ("ulMyHealth", c_ulong),
                ("eMyRefType", c_uint),
                ("sMyRefID", c_char*5),
                ]


# noinspection PyTypeChecker
class EXTVERSION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("Version_eComponentType", c_uint),
                ("Version_szModelName", c_char*16),
                ("Version_szPSN", c_char*16),
                ("Version_szHardwareVersion", c_char*16),
                ("Version_szSoftwareVersion", c_char*16),
                ("Version_szBootVersion", c_char*16),
                ("Version_szCompileDate", c_char*12),
                ("Version_szCompileTime", c_char*12),
                ]


# noinspection PyTypeChecker
class MARKPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class CURRENTSET(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("FileName", c_char*12),
                ("FilePacket", c_ulong),
                ("DumpMode", c_uint),
                ("Group", c_char*12),
                ]


# noinspection PyTypeChecker
class PDCSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("PDCError", c_ulong),
                ("PDCStatus", c_ulong),
                ("BattA", c_float),
                ("BattB", c_float),
                ("BattExt", c_float),
                ("Temp", c_float),
                ("DiskSpace", c_ulong),
                ("Reserved1", c_float),
                ("Reserved2", c_float),
                ]


# noinspection PyTypeChecker
class HIGHRATEL1DATA_aclObservations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPRN", c_ushort),
                ("dMyWideBandADR", c_double),
                ]


# noinspection PyTypeChecker
class HIGHRATEL1DATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclObservations_arraylength", c_ulong),
                ("aclObservations", HIGHRATEL1DATA_aclObservations*325),
                ]


# noinspection PyTypeChecker
class DEBUGPROCESSIDLES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("adMyIdleTimes_Len", c_ulong),
                ("adMyIdleTimes", c_double*480),
                ]


# noinspection PyTypeChecker
class DEBUGPROCESSNAMES_aclMyProcessNameArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyProcessPriority", c_ulong),
                ("szMyProcessorBinding", c_char*16),
                ("szMyProcessName", c_char*32),
                ]


# noinspection PyTypeChecker
class DEBUGPROCESSNAMES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyProcessNameArray_arraylength", c_ulong),
                ("aclMyProcessNameArray", DEBUGPROCESSNAMES_aclMyProcessNameArray*128),
                ]


# noinspection PyTypeChecker
class RXHWLEVELS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("HwLevels_fMyTemperature", c_float),
                ("HwLevels_fMyAntennaCurrent", c_float),
                ("HwLevels_fMyLowVoltage", c_float),
                ("HwLevels_fMySupplyVoltage", c_float),
                ("HwLevels_fMyRFVoltage", c_float),
                ("HwLevels_fMyInternalLNAVoltage", c_float),
                ("HwLevels_fMyReserved1", c_float),
                ("HwLevels_fMyReserved2", c_float),
                ("HwLevels_fMyReserved3", c_float),
                ("HwLevels_fMyLNAOutputVoltage", c_float),
                ]


# noinspection PyTypeChecker
class RTCAIN_clMyRTCAData_Corrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("PseudorangeCorrection", c_double),
                ("IssueofData", c_char),
                ("RangeRateCorrection", c_double),
                ("UDRE", c_float),
                ]


# noinspection PyTypeChecker
class RTCAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clHeader_clMyRTCAData_ulMessageIdentifier", c_ulong),
                ("clHeader_clMyRTCAData_ulRefStation", c_ulong),
                ("clHeader_clMyRTCAData_ulMessageType", c_ulong),
                ("clHeader_clMyRTCAData_ulReserved", c_ulong),
                ("clHeader_clMyRTCAData_ulMessageLength", c_ulong),
                ("clMyRTCAData_ModifiedZCount", c_double),
                ("clMyRTCAData_AEB", c_char),
                ("clMyRTCAData_Corrections_arraylength", c_ulong),
                ("clMyRTCAData_Corrections", RTCAIN_clMyRTCAData_Corrections*72),
                ]


# noinspection PyTypeChecker
class NVMSTATS_DataTable(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eType", c_uint),
                ("ulSubType", c_ulong),
                ]


# noinspection PyTypeChecker
class NVMSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulBlockInUse", c_ulong),
                ("ulVersion", c_ulong),
                ("ulEraseCycles1", c_ulong),
                ("ulBytesLeft1", c_ulong),
                ("ulNextAvailAddr1", c_ulong),
                ("ulEraseCycles2", c_ulong),
                ("ulBytesLeft2", c_ulong),
                ("ulNextAvailAddr2", c_ulong),
                ("DataTable_arraylength", c_ulong),
                ("DataTable", NVMSTATS_DataTable*850),
                ]


# noinspection PyTypeChecker
class CTRLSUM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dOffset", c_double),
                ("dOffsetStd", c_double),
                ("dUTCOffset", c_double),
                ("ulUTCYear", c_ulong),
                ("ucUTCMonth", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCHour", c_char),
                ("ucUTCMinute", c_char),
                ("ulUTCMillisecond", c_ulong),
                ("UTCTimeStatus", c_uint),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySolutionsRTK_ucMyNumHighSats", c_char),
                ("clMySolutionsRTK_ucMyNumHighL2Sats", c_char),
                ("fMyElevationCutoffAngle", c_float),
                ("fMyAngle", c_float),
                ("PDCStatus", c_ulong),
                ("PDCError", c_ulong),
                ("fFloat", c_float),
                ("fFloat", c_float),
                ]


# noinspection PyTypeChecker
class VALIDMODELS_Models(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szModel", c_char*16),
                ("ulMyExpiryYear", c_ulong),
                ("ucMyExpiryMonth", c_ulong),
                ("ucMyExpiryDay", c_ulong),
                ]


# noinspection PyTypeChecker
class VALIDMODELS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("Models_arraylength", c_ulong),
                ("Models", VALIDMODELS_Models*24),
                ]


# noinspection PyTypeChecker
class SAVEDERROR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ScafString", c_char*100),
                ]


# noinspection PyTypeChecker
class AUDIODEF_EventArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("AudioEvent", c_uint),
                ("Volume", c_ulong),
                ("Pitch", c_ulong),
                ]


# noinspection PyTypeChecker
class AUDIODEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("EventArray_arraylength", c_ulong),
                ("EventArray", AUDIODEF_EventArray*10),
                ]


# noinspection PyTypeChecker
class HWLEVELS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("RxHwLevels_fMyTemperature", c_float),
                ("RxHwLevels_fMyAntennaCurrent", c_float),
                ("RxHwLevels_fMyLowVoltage", c_float),
                ("RxHwLevels_fMySupplyVoltage", c_float),
                ("RxHwLevels_fMyRFVoltage", c_float),
                ("RxHwLevels_fMyInternalLNAVoltage", c_float),
                ("RxHwLevels_fMyReserved1", c_float),
                ("RxHwLevels_fMyReserved2", c_float),
                ("RxHwLevels_fMyReserved3", c_float),
                ("RxHwLevels_fMyLNAOutputVoltage", c_float),
                ("BatA", c_float),
                ("BatB", c_float),
                ("BatExt", c_float),
                ("CTemp", c_float),
                ("DiskSpace", c_ulong),
                ("Reserved4", c_float),
                ("Reserved5", c_float),
                ]


# noinspection PyTypeChecker
class RTKDATA_clMyMatchedModel_aclMyRTKSatInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPrn", satelliteid),
                ("eMyAmbiguityType", c_uint),
                ("fMyResidual", c_float),
                ]


# noinspection PyTypeChecker
class RTKDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyMatchedModel_ulMyRTKInfo", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("cCharAsInt", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ("clMyMatchedModel_eMySearchStatus", c_uint),
                ("clMyMatchedModel_ulMyNumLanes", c_ulong),
                ("clMyMatchedModel_afMyCovariance", c_float*9),
                ("clMyFloatBaseline_clMyMatchedModel_dMyX", c_double),
                ("clMyFloatBaseline_clMyMatchedModel_dMyY", c_double),
                ("clMyFloatBaseline_clMyMatchedModel_dMyZ", c_double),
                ("clMyFloatStdDev_clMyMatchedModel_fMyXStdDev", c_float),
                ("clMyFloatStdDev_clMyMatchedModel_fMyYStdDev", c_float),
                ("clMyFloatStdDev_clMyMatchedModel_fMyZStdDev", c_float),
                ("clMyMatchedModel_ulMyRefPrn", c_ulong),
                ("clMyMatchedModel_aclMyRTKSatInfo_arraylength", c_ulong),
                ("clMyMatchedModel_aclMyRTKSatInfo", RTKDATA_clMyMatchedModel_aclMyRTKSatInfo*72),
                ]


# noinspection PyTypeChecker
class RTKVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class GPALM_aclMySVAlmData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulPRN", c_ulong),
                ("ulMyWn", c_ulong),
                ("ulMyHealth8", c_ulong),
                ("dMyEcc", c_double),
                ("dMyTOA", c_double),
                ("dMyDi", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyA", c_double),
                ("dMyOmega", c_double),
                ("dMyOmega0", c_double),
                ("dMyMo", c_double),
                ("dMyAf0", c_double),
                ("dMyAf1", c_double),
                ]


# noinspection PyTypeChecker
class GPALM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySVAlmData_arraylength", c_ulong),
                ("aclMySVAlmData", GPALM_aclMySVAlmData*32),
                ]


# noinspection PyTypeChecker
class GPGGA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("ulMyGGAQuality", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ]


# noinspection PyTypeChecker
class GPGLL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ]


# noinspection PyTypeChecker
class GPGRS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("dMyResidual", c_double),
                ]


# noinspection PyTypeChecker
class GPGRS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class GPGRS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", GPGRS_aclMyEntries*325),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", GPGRS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ("eMyNMEAVersion", c_uint),
                ("eMyIncludeSBAS", c_uint),
                ("eMySource", c_uint),
                ]


# noinspection PyTypeChecker
class GPGSA_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class GPGSA_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class GPGSA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", GPGSA_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", GPGSA_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyVDOP", c_float),
                ("eMyFixCmd", c_uint),
                ("eMyNMEAVersion", c_uint),
                ("eMyIncludeSBAS", c_uint),
                ("eMySource", c_uint),
                ]


# noinspection PyTypeChecker
class GPGST_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("dMyObsStdDev", c_double),
                ]


# noinspection PyTypeChecker
class GPGST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCovariance_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_adMyElements", c_double*9),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", GPGST_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class GPGSV_aclMySatVisList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatID_eMySystemType", c_uint),
                ("clMySatID_idMyID", satelliteid),
                ("dMyElevation", c_double),
                ("dMyAzimuth", c_double),
                ]


# noinspection PyTypeChecker
class GPGSV_clMyObsBase_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("idMyID", satelliteid),
                ("fMyUserCNo", c_float),
                ("ulMyCStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class GPGSV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("aclMySatVisList_arraylength", c_ulong),
                ("aclMySatVisList", GPGSV_aclMySatVisList*39),
                ("clMyObsBase_aclMyObs_arraylength", c_ulong),
                ("clMyObsBase_aclMyObs", GPGSV_clMyObsBase_aclMyObs*325),
                ("eMyEnable", c_uint),
                ("bMyHasGPS", c_bool),
                ("eMyIncludeSBAS", c_uint),
                ]


# noinspection PyTypeChecker
class GPRMB(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("eMyNavStatus", c_uint),
                ("dMyXTrack", c_double),
                ("szMyFromPoint", c_char*6),
                ("szMyToPoint", c_char*6),
                ("dMyToLatitude", c_double),
                ("dMyToLongitude", c_double),
                ("dMyDistance", c_double),
                ("dMyBearing", c_double),
                ("dMyAlongTrackVelocity", c_double),
                ("fMyDeclination", c_float),
                ]


# noinspection PyTypeChecker
class GPRMC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCMonth", c_char),
                ("ulUTCYear", c_ulong),
                ("UTCTimeStatus", c_uint),
                ("fMyDeclination", c_float),
                ("eMyEnableGPRMCAltitude", c_uint),
                ("eMyNMEATime", c_uint),
                ]


# noinspection PyTypeChecker
class GPVTG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyType", c_uint),
                ("eMyStatus", c_uint),
                ("clMyVelocity_dMyGroundTrack", c_double),
                ("clMyVelocity_dMyHorizontalSpeed", c_double),
                ("clMySolutionSatelliteInfo_ucMySystemSet", c_char),
                ("fMyDeclination", c_float),
                ("eMyNMEAVersion", c_uint),
                ]


# noinspection PyTypeChecker
class GPZDA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucUTCDay", c_char),
                ("ucUTCMonth", c_char),
                ("ulUTCYear", c_ulong),
                ("UTCTimeStatus", c_uint),
                ]


# noinspection PyTypeChecker
class MARKTIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyWeek", c_long),
                ("dMySeconds", c_double),
                ("dMyOffset", c_double),
                ("dMyOffsetStd", c_double),
                ("dMyUTCOffset", c_double),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class SLEEPMODE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eSubsystem", c_uint),
                ("eSleepStatus", c_uint),
                ("ulTimeOut", c_ulong),
                ("ulActivity", c_ulong),
                ]


# noinspection PyTypeChecker
class BESTXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("eMyStatus", c_uint),
                ("eMyType", c_uint),
                ("clMyVelocity_clMyECEF_clMyVelocity_dMyX", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_dMyY", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_dMyZ", c_double),
                ("clMyStdDev_clMyECEF_clMyVelocity_fMyXStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_fMyYStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class MATCHEDXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PSRXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class RTKXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class AUXDEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulBPS", c_ulong),
                ("eParity", c_uint),
                ("ulData", c_ulong),
                ("ulStop", c_ulong),
                ("eHandshake", c_uint),
                ("eEcho", c_uint),
                ("cStartLength", c_char),
                ("szStart", c_char*3),
                ("cStopLength", c_char),
                ("szStop", c_char*3),
                ("ulTimeOut", c_ulong),
                ("ulPacketSize", c_ulong),
                ("eMark", c_uint),
                ]


# noinspection PyTypeChecker
class BATSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulBatStatus", c_ulong),
                ("fBatAVolt", c_float),
                ("fBatBVolt", c_float),
                ("fExtVolt", c_float),
                ("fBatALife", c_float),
                ("fBatBLife", c_float),
                ("ulAux2", c_ulong),
                ("ulAux3", c_ulong),
                ("ulBatACutoff", c_ulong),
                ("ulBatBCutoff", c_ulong),
                ("ulExtCutoff", c_ulong),
                ("ulRes4", c_ulong),
                ("ulRes5", c_ulong),
                ("ulRes6", c_ulong),
                ]


# noinspection PyTypeChecker
class PDCSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulError", c_ulong),
                ("ulStatus", c_ulong),
                ("fBatALife", c_float),
                ("fBatBLife", c_float),
                ("fExtVolt", c_float),
                ("fTemp", c_float),
                ("ulDiskSpace", c_ulong),
                ("ulExtError", c_ulong),
                ("ulExtStatus", c_ulong),
                ("ulMinStack", c_ulong),
                ("ulMinTask", c_ulong),
                ("ulHeap", c_ulong),
                ("ulGPSStatus", c_ulong),
                ("fBatAVolt", c_float),
                ("fBatBVolt", c_float),
                ("Res1", c_long),
                ("Res2", c_ulong),
                ("Res3", c_ulong),
                ("Res4", c_float),
                ("Res5", c_char*24),
                ]


# noinspection PyTypeChecker
class GPGGARTK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("ulMyGGAQuality", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM1819_clMyRTCM18_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("lMyAdr", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1819_clMyRTCM19_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyPsr", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM1819(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM18_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyHealth", c_ulong),
                ("clMyRTCM18_ulMyFreq", c_ulong),
                ("clMyRTCM18_ulMySpare", c_ulong),
                ("clMyRTCM18_lMyTime", c_long),
                ("clMyRTCM18_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM18_aclMyRTCMBody", RTCM1819_clMyRTCM18_aclMyRTCMBody*15),
                ("clMyRTCMHeader_clMyRTCM19_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyHealth", c_ulong),
                ("clMyRTCM19_ulMyFreq", c_ulong),
                ("clMyRTCM19_ulMySmoothingInterval", c_ulong),
                ("clMyRTCM19_lMyTime", c_long),
                ("clMyRTCM19_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM19_aclMyRTCMBody", RTCM1819_clMyRTCM19_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class OPTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ModelOptionsClass_ulMyLowBits", c_ulong),
                ("ModelOptionsClass_ulMyHighBits", c_ulong),
                ]


# noinspection PyTypeChecker
class INSATT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSCOV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyCovariance_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_adMyElements", c_double*9),
                ("clMyCovariance_clMyAttitude_clMyPVASolution_adMyElements", c_double*9),
                ("clMyCovariance_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_adMyElements", c_double*9),
                ]


# noinspection PyTypeChecker
class INSPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSSPD(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class RAWIMU(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRawIMUData_ulMyGPSWeek", c_ulong),
                ("clMyRawIMUData_dMyGPSSeconds", c_double),
                ("clMyRawIMUData_ulMyIMUStatus", c_ulong),
                ("clMyRawIMUData_alMyExternalIMUObs", c_long*6),
                ]


# noinspection PyTypeChecker
class SATXYZ_aclMySats(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyXYZRB_dMyX", c_double),
                ("clMyXYZRB_dMyY", c_double),
                ("clMyXYZRB_dMyZ", c_double),
                ("clMyXYZRB_dMyRB", c_double),
                ("dMyIonoCorr", c_double),
                ("dMyTropoCorr", c_double),
                ("dMyDummy", c_double),
                ("dMyDummy", c_double),
                ]


# noinspection PyTypeChecker
class SATXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dDouble", c_double),
                ("aclMySats_arraylength", c_ulong),
                ("aclMySats", SATXYZ_aclMySats*72),
                ]


# noinspection PyTypeChecker
class CHANDEBUGFFTPHASE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("afMyPhase_Len", c_ulong),
                ("afMyPhase", c_float*500),
                ]


# noinspection PyTypeChecker
class CHANDEBUGFFTPOWER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("afMyPower_Len", c_ulong),
                ("afMyPower", c_float*500),
                ]


# noinspection PyTypeChecker
class ISMR_aclMyReducedDataEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPrn", c_ulong),
                ("fMyAzimuth", c_float),
                ("fMyAltitude", c_float),
                ("dMyCNo", c_double),
                ("dMyS4", c_double),
                ("dMyS4Correction", c_double),
                ("dMy1SecStdDev", c_double),
                ("dMy3SecStdDev", c_double),
                ("dMy10SecStdDev", c_double),
                ("dMy30SecStdDev", c_double),
                ("dMy60SecStdDev", c_double),
                ("dMyAverageIonDivergence", c_double),
                ("dMyAverageIonDivergenceStdDev", c_double),
                ("fMyTOW15TEC", c_float),
                ("fMyTOW15DeltaTEC", c_float),
                ("fMyTOW30TEC", c_float),
                ("fMyTOW30DeltaTEC", c_float),
                ("fMyTOW45TEC", c_float),
                ("fMyTOW45DeltaTEC", c_float),
                ("fMyTOWTEC", c_float),
                ("fMyTOWDeltaTEC", c_float),
                ("dMyLockTime", c_double),
                ("ulMyStatus", c_ulong),
                ("dMyL2LockTime", c_double),
                ("dMyL2CNo", c_double),
                ]


# noinspection PyTypeChecker
class ISMR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyReducedDataEntries_arraylength", c_ulong),
                ("aclMyReducedDataEntries", ISMR_aclMyReducedDataEntries*20),
                ]


# noinspection PyTypeChecker
class RTCM9_clMyRTCM9_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM9(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM9_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM9_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMyHealth", c_ulong),
                ("clMyRTCM9_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM9_aclMyDiffData", RTCM9_clMyRTCM9_aclMyDiffData*325),
                ]


# noinspection PyTypeChecker
class RTCM9IN_clMyRTCM_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM9IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyHealth", c_ulong),
                ("clMyRTCM_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM_aclMyDiffData", RTCM9IN_clMyRTCM_aclMyDiffData*325),
                ]


# noinspection PyTypeChecker
class POINT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPointLogData_fMyDifferentialLag", c_float),
                ("clMyPointLogData_ucMyNumObsUsedInSol", c_char),
                ("clMyPointLogData_ucMyNumHighL1Sats", c_char),
                ("clMyPointLogData_ucMyNumHighL2Sats", c_char),
                ("clMyPointLogData_dMyLatitude", c_double),
                ("clMyPointLogData_dMyLongitude", c_double),
                ("clMyPointLogData_dMyHeight", c_double),
                ("clMyPointLogData_dMyDeltaNorth", c_double),
                ("clMyPointLogData_dMyDeltaEast", c_double),
                ("clMyPointLogData_dMyDeltaUp", c_double),
                ("clMyPointLogData_fMySDev2D", c_float),
                ("clMyPointLogData_fMySDev3D", c_float),
                ("clMyPointLogData_fMySDev1D", c_float),
                ("clMyPointLogData_dMyAzimuth", c_double),
                ("clMyPointLogData_dMyElevation", c_double),
                ("clMyPointLogData_fMySlopeDistance", c_float),
                ("clMyPointLogData_eMyPositionStatus", c_uint),
                ("clMyPointLogData_eMyPositionType", c_uint),
                ("clMyPointLogData_acMyStationID", c_char*4),
                ]


# noinspection PyTypeChecker
class BASESTATIONOBS_clMyObservationsBase_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySvPrn", c_ushort),
                ("usMySvFreq", c_ushort),
                ("dMyPsr", c_double),
                ("fMyVPsr", c_float),
                ("dMyAdr", c_double),
                ("fMyVAdr", c_float),
                ("fMyDop", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ("fMyDAcc", c_float),
                ("eMyFreq", c_uint),
                ("sigMyChan", c_int),
                ("fMyUserCNo", c_float),
                ]


# noinspection PyTypeChecker
class BASESTATIONOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMessageEnum", c_uint),
                ("acMyDiffStationID", c_char*4),
                ("clMyCoords_clMyXYZ_clMyPosition_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_dMyZ", c_double),
                ("clMyObservationsBase_ulMyWN", c_ulong),
                ("clMyObservationsBase_dMyRecTime", c_double),
                ("clMyObservationsBase_aclMyObs_arraylength", c_ulong),
                ("clMyObservationsBase_aclMyObs", BASESTATIONOBS_clMyObservationsBase_aclMyObs*325),
                ]


# noinspection PyTypeChecker
class SATXYZOCC_aclMySats(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("fMyElevation", c_float),
                ("clMyXYZRB_dMyX", c_double),
                ("clMyXYZRB_dMyY", c_double),
                ("clMyXYZRB_dMyZ", c_double),
                ("dMyIonoCorr", c_double),
                ("fMyLockTimeL1", c_float),
                ("fMyLockTimeL2", c_float),
                ]


# noinspection PyTypeChecker
class SATXYZOCC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySats_arraylength", c_ulong),
                ("aclMySats", SATXYZOCC_aclMySats*72),
                ]


# noinspection PyTypeChecker
class RTCM16T(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyText", c_char*90),
                ]


# noinspection PyTypeChecker
class BASERANGE_clMyObservationsBase_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySvPrn", c_ushort),
                ("usMySvFreq", c_ushort),
                ("dMyPsr", c_double),
                ("fMySDPsr", c_float),
                ("dMyAdr", c_double),
                ("fMySDAdr", c_float),
                ("fMyDop", c_float),
                ("fMyUserCNo", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class BASERANGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyObservationsBase_aclMyObs_arraylength", c_ulong),
                ("clMyObservationsBase_aclMyObs", BASERANGE_clMyObservationsBase_aclMyObs*325),
                ]


# noinspection PyTypeChecker
class BESTPVC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ]


# noinspection PyTypeChecker
class POSVELNAVDOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("eMyNavStatus", c_uint),
                ("dMyLatOrigin", c_double),
                ("dMyLonOrigin", c_double),
                ("dMyLatDestination", c_double),
                ("dMyLonDestination", c_double),
                ("dMyXTrack", c_double),
                ("dMyAlongTrack", c_double),
                ("fMyXTrackStdDev", c_float),
                ("fMyAlongTrackStdDev", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ]


# noinspection PyTypeChecker
class RAWWAASFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iMyFrameDecoderNum", c_int),
                ("ulMyPrn", c_ulong),
                ("ulMyWAASMsgId", c_ulong),
                ("aucMyRawFrameData", c_char*29),
                ("ulMySignalChannelNum", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS0(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("aucMyPRNMask", c_char*27),
                ("ulMyIODP", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS10(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyBrrc", c_ulong),
                ("ulMyCltc_lsb", c_ulong),
                ("ulMyCltc_v1", c_ulong),
                ("ulMyIltc_v1", c_ulong),
                ("ulMyCltc_v0", c_ulong),
                ("ulMyIltc_v0", c_ulong),
                ("ulMyCgeo_lsb", c_ulong),
                ("ulMyCgeo_v", c_ulong),
                ("ulMyIgeo", c_ulong),
                ("ulMyCer", c_ulong),
                ("ulMyCiono_step", c_ulong),
                ("ulMyIiono", c_ulong),
                ("ulMyCiono_ramp", c_ulong),
                ("ulMyRSSUDRE", c_ulong),
                ("ulMyRSSIono", c_ulong),
                ("aulMySpareBits", c_char*11),
                ]


# noinspection PyTypeChecker
class WAAS12(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("dMyA1", c_double),
                ("dMyA0", c_double),
                ("ulMyt0t", c_ulong),
                ("usMyWN", c_ushort),
                ("sMyDtLS", c_short),
                ("usMyWNLSF", c_ushort),
                ("usMyDN", c_ushort),
                ("usMyDtLSF", c_short),
                ("usMyUTCID", c_ushort),
                ("ulMyGPSTOW", c_ulong),
                ("ulMyGPSWN", c_ulong),
                ("bMyGlonassIndicator", c_bool),
                ("aucMyReservedBits", c_char*10),
                ]


# noinspection PyTypeChecker
class WAAS17_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyDataID", c_ushort),
                ("usMyPRN", c_ushort),
                ("usMyHealth", c_ushort),
                ("lMyX", c_long),
                ("lMyY", c_long),
                ("lMyZ", c_long),
                ("lMyXVel", c_long),
                ("lMyYVel", c_long),
                ("lMyZVel", c_long),
                ]


# noinspection PyTypeChecker
class WAAS17(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", WAAS17_aclMyEntries*3),
                ("ulMyt0", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS18(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyNumBands", c_ulong),
                ("ulMyBandNum", c_ulong),
                ("ulMyIODI", c_ulong),
                ("aucMyIGPMask", c_char*26),
                ("ulMySpareBit", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class WAAS24(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("alMyPRC", c_long*6),
                ("aulMyUDREI", c_ulong*6),
                ("ulMyIODP", c_ulong),
                ("ulMyBlockID", c_ulong),
                ("ulMyIODF", c_ulong),
                ("ulMySpare", c_ulong),
                ("clMySlowCorrections_ulMyVelocityCode", c_ulong),
                ("clMySlowCorrections_ulMyPRNMaskNumber1", c_ulong),
                ("clMySlowCorrections_ulMyIODE1", c_ulong),
                ("clMySlowCorrections_lMyDX1", c_long),
                ("clMySlowCorrections_lMyDY1", c_long),
                ("clMySlowCorrections_lMyDZ1", c_long),
                ("clMySlowCorrections_lMyaF01", c_long),
                ("clMySlowCorrections_ulMyPRNMaskNumber2", c_ulong),
                ("clMySlowCorrections_ulMyIODE2", c_ulong),
                ("clMySlowCorrections_lMyDX2orDDX", c_long),
                ("clMySlowCorrections_lMyDY2orDDY", c_long),
                ("clMySlowCorrections_lMyDZ2orDDZ", c_long),
                ("clMySlowCorrections_lMyaF02oraF1", c_long),
                ("clMySlowCorrections_ulMyTOD", c_ulong),
                ("clMySlowCorrections_ulMyIODP", c_ulong),
                ("clMySlowCorrections_ulMySpare", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS25(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFirstHalf_ulMyVelocityCode", c_ulong),
                ("clMyFirstHalf_ulMyPRNMaskNumber1", c_ulong),
                ("clMyFirstHalf_ulMyIODE1", c_ulong),
                ("clMyFirstHalf_lMyDX1", c_long),
                ("clMyFirstHalf_lMyDY1", c_long),
                ("clMyFirstHalf_lMyDZ1", c_long),
                ("clMyFirstHalf_lMyaF01", c_long),
                ("clMyFirstHalf_ulMyPRNMaskNumber2", c_ulong),
                ("clMyFirstHalf_ulMyIODE2", c_ulong),
                ("clMyFirstHalf_lMyDX2orDDX", c_long),
                ("clMyFirstHalf_lMyDY2orDDY", c_long),
                ("clMyFirstHalf_lMyDZ2orDDZ", c_long),
                ("clMyFirstHalf_lMyaF02oraF1", c_long),
                ("clMyFirstHalf_ulMyTOD", c_ulong),
                ("clMyFirstHalf_ulMyIODP", c_ulong),
                ("clMyFirstHalf_ulMySpare", c_ulong),
                ("clMySecondHalf_ulMyVelocityCode", c_ulong),
                ("clMySecondHalf_ulMyPRNMaskNumber1", c_ulong),
                ("clMySecondHalf_ulMyIODE1", c_ulong),
                ("clMySecondHalf_lMyDX1", c_long),
                ("clMySecondHalf_lMyDY1", c_long),
                ("clMySecondHalf_lMyDZ1", c_long),
                ("clMySecondHalf_lMyaF01", c_long),
                ("clMySecondHalf_ulMyPRNMaskNumber2", c_ulong),
                ("clMySecondHalf_ulMyIODE2", c_ulong),
                ("clMySecondHalf_lMyDX2orDDX", c_long),
                ("clMySecondHalf_lMyDY2orDDY", c_long),
                ("clMySecondHalf_lMyDZ2orDDZ", c_long),
                ("clMySecondHalf_lMyaF02oraF1", c_long),
                ("clMySecondHalf_ulMyTOD", c_ulong),
                ("clMySecondHalf_ulMyIODP", c_ulong),
                ("clMySecondHalf_ulMySpare", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS26_aclMyGridPointData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyIGPVDE", c_ulong),
                ("ulMyGIVEI", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS26(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyBandNum", c_ulong),
                ("ulMyBlockID", c_ulong),
                ("aclMyGridPointData_arraylength", c_ulong),
                ("aclMyGridPointData", WAAS26_aclMyGridPointData*15),
                ("ulMyIODI", c_ulong),
                ("ulMySpareBits", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS27_aclMyRegions(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyLat1", c_long),
                ("lMyLong1", c_long),
                ("lMyLat2", c_long),
                ("lMyLong2", c_long),
                ("ulMyShape", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS27(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODS", c_ulong),
                ("ulMyNumServiceMsgs", c_ulong),
                ("ulMyServiceMsgNum", c_ulong),
                ("ulMyPriorityCode", c_ulong),
                ("ulMyUDREInside", c_ulong),
                ("ulMyUDREOutside", c_ulong),
                ("aclMyRegions_arraylength", c_ulong),
                ("aclMyRegions", WAAS27_aclMyRegions*5),
                ("ulMyt0", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class WAAS4(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class WAAS5(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class WAAS6(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODF2", c_ulong),
                ("ulMyIODF3", c_ulong),
                ("ulMyIODF4", c_ulong),
                ("ulMyIODF5", c_ulong),
                ("aulMyUDREI", c_ulong*51),
                ]


# noinspection PyTypeChecker
class WAAS7(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMySystemLatency", c_ulong),
                ("ulMyIODP", c_ulong),
                ("ulMySpareBits", c_ulong),
                ("aulMyDegradationFactor", c_ulong*51),
                ]


# noinspection PyTypeChecker
class WAAS9(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODN", c_ulong),
                ("ulMyt0", c_ulong),
                ("ulMyURA", c_ulong),
                ("dMyX", c_double),
                ("dMyY", c_double),
                ("dMyZ", c_double),
                ("dMyXVel", c_double),
                ("dMyYVel", c_double),
                ("dMyZVel", c_double),
                ("dMyXAccel", c_double),
                ("dMyYAccel", c_double),
                ("dMyZAccel", c_double),
                ("dMyaf0", c_double),
                ("dMyaf1", c_double),
                ]


# noinspection PyTypeChecker
class RTCM15_clMyRTCM15_acMyIonData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyReserved", c_ulong),
                ("ulMyGpsGlonass", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("ulMyCor", c_ulong),
                ("iMyCorrate", c_int),
                ]


# noinspection PyTypeChecker
class RTCM15(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM15_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM15_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyHealth", c_ulong),
                ("clMyRTCM15_acMyIonData_arraylength", c_ulong),
                ("clMyRTCM15_acMyIonData", RTCM15_clMyRTCM15_acMyIonData*325),
                ]


# noinspection PyTypeChecker
class RTCM15IN_clMyRTCM15_acMyIonData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyReserved", c_ulong),
                ("ulMyGpsGlonass", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("ulMyCor", c_ulong),
                ("iMyCorrate", c_int),
                ]


# noinspection PyTypeChecker
class RTCM15IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM15_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM15_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyHealth", c_ulong),
                ("clMyRTCM15_acMyIonData_arraylength", c_ulong),
                ("clMyRTCM15_acMyIonData", RTCM15IN_clMyRTCM15_acMyIonData*325),
                ]


# noinspection PyTypeChecker
class ENVIRONMENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("HwLevels_fMyAntennaCurrent", c_float),
                ("HwLevels_fMyLowVoltage", c_float),
                ("HwLevels_fMySupplyVoltage", c_float),
                ("HwLevels_fMyRFVoltage", c_float),
                ("HwLevels_fMyInternalLNAVoltage", c_float),
                ("HwLevels_fMyLNAOutputVoltage", c_float),
                ("HwLevels_fMyReserved1", c_float),
                ("HwLevels_fMyReserved2", c_float),
                ("HwLevels_fMyReserved3", c_float),
                ("HwLevels_fMyTemperature", c_float),
                ("HwLevels_fMyExternalTemperature", c_float),
                ("HwLevels_fMyAirPressure", c_float),
                ("HwLevels_fMyHumidity", c_float),
                ("HwLevels_fMyWindSpeed", c_float),
                ("HwLevels_fMyWindDirection", c_float),
                ]


# noinspection PyTypeChecker
class CMRDESC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clType2Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clType2Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clType2Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clType2Message_ulMyLength", c_ulong),
                ("clType2Message_ulMyVersion", c_ulong),
                ("clType2Message_ulMyStationID", c_ulong),
                ("clType2Message_ulMyMessageType", c_ulong),
                ("clType2Message_bMyIsBatteryLow", c_bool),
                ("clType2Message_bMyIsMemLow", c_bool),
                ("clType2Message_ulMyReserved1", c_ulong),
                ("clType2Message_bMyIsL2Enabled", c_bool),
                ("clType2Message_ulMyReserved2", c_ulong),
                ("clType2Message_ulMyEpochTime", c_ulong),
                ("clType2Message_ulMyMotionState", c_ulong),
                ("clType2Message_ulMyAntennaNumber", c_ulong),
                ("clMyCMRBody_clType2Message_ulMyRecLength", c_ulong),
                ("clMyCMRBody_clType2Message_aucMyShortID", c_char*8),
                ("clMyCMRBody_clType2Message_aucMyCOGOCode", c_char*16),
                ("clMyCMRBody_clType2Message_aucMyLongID_Len", c_ulong),
                ("clMyCMRBody_clType2Message_aucMyLongID", c_char*51),
                ]


# noinspection PyTypeChecker
class POSVELNAV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("eMyNavStatus", c_uint),
                ("dMyDistance", c_double),
                ("dMyBearing", c_double),
                ("dMyAlongTrack", c_double),
                ("dMyXTrack", c_double),
                ("ulMyETAWeeks", c_ulong),
                ("dMyETASeconds", c_double),
                ]


# noinspection PyTypeChecker
class WAASCORR_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODE", c_ulong),
                ("fMyCorrection", c_float),
                ("fMyStdDev", c_float),
                ]


# noinspection PyTypeChecker
class WAASCORR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", WAASCORR_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class COMCONFIG_aclMyComConfig(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("ulMyBaud", c_ulong),
                ("eMyParity", c_uint),
                ("ulMyDataBits", c_ulong),
                ("ulMyStopBits", c_ulong),
                ("eMyHandshake", c_uint),
                ("eMyEcho", c_uint),
                ("eMyBreaks", c_uint),
                ("eMyRXType", c_uint),
                ("eMyTXType", c_uint),
                ("eMyResponses", c_uint),
                ]


# noinspection PyTypeChecker
class COMCONFIG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyComConfig_arraylength", c_ulong),
                ("aclMyComConfig", COMCONFIG_aclMyComConfig*53),
                ]


# noinspection PyTypeChecker
class INSATTS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSCOVS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyCovariance_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_adMyElements", c_double*9),
                ("clMyCovariance_clMyAttitude_clMyPVASolution_adMyElements", c_double*9),
                ("clMyCovariance_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_adMyElements", c_double*9),
                ]


# noinspection PyTypeChecker
class INSPOSS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSPOSSYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dSeconds", c_double),
                ("clEcefPosition_dMyX", c_double),
                ("clEcefPosition_dMyY", c_double),
                ("clEcefPosition_dMyZ", c_double),
                ("adEcefCovariance", c_double*9),
                ]


# noinspection PyTypeChecker
class INSSPDS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSVELS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class RAWIMUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRawIMUData_ulMyGPSWeek", c_ulong),
                ("clMyRawIMUData_dMyGPSSeconds", c_double),
                ("clMyRawIMUData_ulMyIMUStatus", c_ulong),
                ("clMyRawIMUData_alMyExternalIMUObs", c_long*6),
                ]


# noinspection PyTypeChecker
class DETRSIN_aclMyScintillationData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPrn", c_ushort),
                ("usMyFrequency", c_ushort),
                ("fMyTEC", c_float),
                ("fMy1SecondDeltaTEC", c_float),
                ("dMyFirstADR", c_double),
                ("alMyScintillationData", c_long*100),
                ]


# noinspection PyTypeChecker
class DETRSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyScintillationData_arraylength", c_ulong),
                ("aclMyScintillationData", DETRSIN_aclMyScintillationData*20),
                ]


# noinspection PyTypeChecker
class RAWSIN_aclMyScintillationData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPrn", c_ushort),
                ("usMyFrequency", c_ushort),
                ("fMyTEC", c_float),
                ("fMy1SecondDeltaTEC", c_float),
                ("dMyFirstADR", c_double),
                ("alMyScintillationData", c_long*100),
                ]


# noinspection PyTypeChecker
class RAWSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyScintillationData_arraylength", c_ulong),
                ("aclMyScintillationData", RAWSIN_aclMyScintillationData*20),
                ]


# noinspection PyTypeChecker
class CLASSELEMLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ClassId", c_ulong),
                ("ElementId", c_ulong),
                ("TypeId", c_ulong),
                ("Length", c_ulong),
                ("Offset", c_ulong),
                ("ChildClassId", c_ulong),
                ("Description", c_char*40),
                ("ElementType", c_ulong),
                ("ArraySize", c_ulong),
                ("ArrayOffset", c_ulong),
                ("ConvertStr", c_char*40),
                ("DefaultValue", c_double),
                ("MinValue", c_double),
                ("MaxValue", c_double),
                ]


# noinspection PyTypeChecker
class CLASSLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ClassIdArray_Len", c_ulong),
                ("ClassIdArray", c_ulong*500),
                ]


# noinspection PyTypeChecker
class CLASSREQLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ClassId", c_ulong),
                ("NumElements", c_ulong),
                ]


# noinspection PyTypeChecker
class ENUMLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("EnumArray_Len", c_ulong),
                ("EnumArray", c_ulong*512),
                ]


# noinspection PyTypeChecker
class ENUMREQLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("Name", c_char*40),
                ]


# noinspection PyTypeChecker
class MSGIDLIST_MsgIdArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("MessageId", c_ulong),
                ("MsgCrc", c_ulong),
                ]


# noinspection PyTypeChecker
class MSGIDLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("MsgIdArray_arraylength", c_ulong),
                ("MsgIdArray", MSGIDLIST_MsgIdArray*100),
                ]


# noinspection PyTypeChecker
class MSGREQLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("MessageId", c_ulong),
                ("MessageName", c_char*32),
                ("Help", c_char*40),
                ("MsgCRC", c_ulong),
                ("Hidden", c_bool),
                ("ParamArray_Len", c_ulong),
                ("ParamArray", c_long*100),
                ]


# noinspection PyTypeChecker
class TYPELIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TypeArray_Len", c_ulong),
                ("TypeArray", c_ulong*100),
                ]


# noinspection PyTypeChecker
class TYPEREQLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TypeId", c_ulong),
                ("Name", c_char*40),
                ("Length", c_ulong),
                ("BaseType", c_ulong),
                ("Description", c_char*40),
                ("Default", c_double),
                ("ElementType", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCAEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAEPHEM_NovAtelDesignator", c_char),
                ("clMyRTCAEPHEM_ucSubtype", c_char),
                ("clMyRTCAEPHEM_ulMyWeek", c_ulong),
                ("clMyRTCAEPHEM_ulMySeconds", c_ulong),
                ("clMyRTCAEPHEM_ulMyPrn", c_ulong),
                ("clMyRTCAEPHEM_ucMyReserved", c_char),
                ("clMyRTCAEPHEM_aucMyRawData", c_char*90),
                ]


# noinspection PyTypeChecker
class RTCAEPHEMIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAHeader_clMyRTCAEPHEM_ulMessageIdentifier", c_ulong),
                ("clMyRTCAHeader_clMyRTCAEPHEM_ulRefStation", c_ulong),
                ("clMyRTCAHeader_clMyRTCAEPHEM_ulMessageType", c_ulong),
                ("clMyRTCAHeader_clMyRTCAEPHEM_ulReserved", c_ulong),
                ("clMyRTCAHeader_clMyRTCAEPHEM_ulMessageLength", c_ulong),
                ("clMyRTCAEPHEM_NovAtelDesignator", c_char),
                ("clMyRTCAEPHEM_ucSubtype", c_char),
                ("clMyRTCAEPHEM_ulMyWeek", c_ulong),
                ("clMyRTCAEPHEM_ulMySeconds", c_ulong),
                ("clMyRTCAEPHEM_ulMyPrn", c_ulong),
                ("clMyRTCAEPHEM_ucMyReserved", c_char),
                ("clMyRTCAEPHEM_aucMyRawData", c_char*90),
                ]


# noinspection PyTypeChecker
class HEIGHTMODELSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMode", c_uint),
                ("szDescription", c_char*64),
                ("szDate", c_char*32),
                ("iNumPoints", c_int),
                ("iNumTriangles", c_int),
                ("iNumTrianglePointers", c_int),
                ("iByteSize", c_int),
                ]


# noinspection PyTypeChecker
class RTCM2021_clMyRTCM20_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("ulIODE", c_ulong),
                ("lPhaseCorr", c_long),
                ]


# noinspection PyTypeChecker
class RTCM2021_clMyRTCM21_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyRateCorrSF", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyPsrCorrSF", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyIODE", c_ulong),
                ("lMyPsrCorr", c_long),
                ("lMyPsrCorrRate", c_long),
                ]


# noinspection PyTypeChecker
class RTCM2021(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM20_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyHealth", c_ulong),
                ("clMyRTCM20_ulMyFreq", c_ulong),
                ("clMyRTCM20_ulSpare", c_ulong),
                ("clMyRTCM20_lMyTime", c_long),
                ("clMyRTCM20_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM20_aclMyRTCMBody", RTCM2021_clMyRTCM20_aclMyRTCMBody*15),
                ("clMyRTCMHeader_clMyRTCM21_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyHealth", c_ulong),
                ("clMyRTCM21_ulMyFreq", c_ulong),
                ("clMyRTCM21_ulMySmoothingInterval", c_ulong),
                ("clMyRTCM21_lMyTime", c_long),
                ("clMyRTCM21_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM21_aclMyRTCMBody", RTCM2021_clMyRTCM21_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class NOISEFLOOR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyNoiseFloor_f1MSNoiseFloorE1", c_float),
                ("clMyNoiseFloor_f1MSNoiseFloorE2", c_float),
                ("clMyNoiseFloor_f1MSNoiseFloorE3", c_float),
                ("clMyNoiseFloor_f1MSNoiseChannelNoiseFloorE1", c_float),
                ("clMyNoiseFloor_f1MSNoiseChannelNoiseFloorE2", c_float),
                ("clMyNoiseFloor_f1MSNoiseChannelNoiseFloorE3", c_float),
                ]


# noinspection PyTypeChecker
class INSBIASES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGyroBiases_dMyX", c_double),
                ("clMyGyroBiases_dMyY", c_double),
                ("clMyGyroBiases_dMyZ", c_double),
                ("clMyGyroBiasStdev_fMyXStdDev", c_float),
                ("clMyGyroBiasStdev_fMyYStdDev", c_float),
                ("clMyGyroBiasStdev_fMyZStdDev", c_float),
                ("clMyAccelBiases_dMyX", c_double),
                ("clMyAccelBiases_dMyY", c_double),
                ("clMyAccelBiases_dMyZ", c_double),
                ("clMyAccelBiasStdev_fMyXStdDev", c_float),
                ("clMyAccelBiasStdev_fMyYStdDev", c_float),
                ("clMyAccelBiasStdev_fMyZStdDev", c_float),
                ]


# noinspection PyTypeChecker
class INSLIGHTS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulLeds", c_ulong),
                ]


# noinspection PyTypeChecker
class INSKCOV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("mdMyEcefPosCov", c_double*9),
                ("mdMyVelCov", c_double*9),
                ("mdMyAttCov", c_double*9),
                ("mdMyLocPosCov", c_double*9),
                ]


# noinspection PyTypeChecker
class INSKINIT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInitialReCov_adMyElements", c_double*9),
                ("clMyInitialVeCov_adMyElements", c_double*9),
                ("clMyInitialAttCov_adMyElements", c_double*9),
                ]


# noinspection PyTypeChecker
class INSKSTATE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGyroBiases_dMyX", c_double),
                ("clMyGyroBiases_dMyY", c_double),
                ("clMyGyroBiases_dMyZ", c_double),
                ("clMyGyroBiasStdev_fMyXStdDev", c_float),
                ("clMyGyroBiasStdev_fMyYStdDev", c_float),
                ("clMyGyroBiasStdev_fMyZStdDev", c_float),
                ("clMyAccelBiases_dMyX", c_double),
                ("clMyAccelBiases_dMyY", c_double),
                ("clMyAccelBiases_dMyZ", c_double),
                ("clMyAccelBiasStdev_fMyXStdDev", c_float),
                ("clMyAccelBiasStdev_fMyYStdDev", c_float),
                ("clMyAccelBiasStdev_fMyZStdDev", c_float),
                ("clMyGyroScaleFactor_dMyX", c_double),
                ("clMyGyroScaleFactor_dMyY", c_double),
                ("clMyGyroScaleFactor_dMyZ", c_double),
                ("clMyGyroScaleFactorStdev_fMyXStdDev", c_float),
                ("clMyGyroScaleFactorStdev_fMyYStdDev", c_float),
                ("clMyGyroScaleFactorStdev_fMyZStdDev", c_float),
                ("clMyAccelScaleFactor_dMyX", c_double),
                ("clMyAccelScaleFactor_dMyY", c_double),
                ("clMyAccelScaleFactor_dMyZ", c_double),
                ("clMyAccelScaleFactorStdev_fMyXStdDev", c_float),
                ("clMyAccelScaleFactorStdev_fMyYStdDev", c_float),
                ("clMyAccelScaleFactorStdev_fMyZStdDev", c_float),
                ("clMyGyroNO_dMyX", c_double),
                ("clMyGyroNO_dMyY", c_double),
                ("clMyGyroNO_dMyZ", c_double),
                ("clMyGyroNOStdev_fMyXStdDev", c_float),
                ("clMyGyroNOStdev_fMyYStdDev", c_float),
                ("clMyGyroNOStdev_fMyZStdDev", c_float),
                ("clMyAccelNO_dMyX", c_double),
                ("clMyAccelNO_dMyY", c_double),
                ("clMyAccelNO_dMyZ", c_double),
                ("clMyAccelNOStdev_fMyXStdDev", c_float),
                ("clMyAccelNOStdev_fMyYStdDev", c_float),
                ("clMyAccelNOStdev_fMyZStdDev", c_float),
                ]


# noinspection PyTypeChecker
class INSSYSTEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyGPSSeconds", c_double),
                ("adMyX", c_double*6),
                ("mdMyAtMidInsEpochRbe", c_double*9),
                ("mdMyEpochRbe", c_double*9),
                ("adMyGe", c_double*3),
                ("adMyWEpoch", c_double*3),
                ("bMyDoZUPT", c_bool),
                ("mdMyRle", c_double*9),
                ("iMyLastUpdateID", c_int),
                ("dMyAccSize", c_double),
                ("dMyGyroSize", c_double),
                ]


# noinspection PyTypeChecker
class CMRDATADESC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clType2Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clType2Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clType2Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clType2Message_ulMyLength", c_ulong),
                ("clType2Message_ulMyVersion", c_ulong),
                ("clType2Message_ulMyStationID", c_ulong),
                ("clType2Message_ulMyMessageType", c_ulong),
                ("clType2Message_bMyIsBatteryLow", c_bool),
                ("clType2Message_bMyIsMemLow", c_bool),
                ("clType2Message_ulMyReserved1", c_ulong),
                ("clType2Message_bMyIsL2Enabled", c_bool),
                ("clType2Message_ulMyReserved2", c_ulong),
                ("clType2Message_ulMyEpochTime", c_ulong),
                ("clType2Message_ulMyMotionState", c_ulong),
                ("clType2Message_ulMyAntennaNumber", c_ulong),
                ("clMyCMRBody_clType2Message_ulMyRecLength", c_ulong),
                ("clMyCMRBody_clType2Message_aucMyShortID", c_char*8),
                ("clMyCMRBody_clType2Message_aucMyCOGOCode", c_char*16),
                ("clMyCMRBody_clType2Message_aucMyLongID_Len", c_ulong),
                ("clMyCMRBody_clType2Message_aucMyLongID", c_char*51),
                ]


# noinspection PyTypeChecker
class CMRDATAOBS_clMyType0Message_aclMyCMRBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySlotNumber", c_ulong),
                ("bMyCodeFlag", c_bool),
                ("bMyL1PhaseValid", c_bool),
                ("bMyIsL2Present", c_bool),
                ("ulMyL1Psr", c_ulong),
                ("lMyL1CarrierOffset", c_long),
                ("ulMyL1Snr", c_ulong),
                ("ulMyL1SlipCount", c_ulong),
                ("bMyIsL2Code", c_bool),
                ("bMyCodeType", c_bool),
                ("bMyIsL2CodeValid", c_bool),
                ("bMyIsL2PhaseValid", c_bool),
                ("bMyPhaseFull", c_bool),
                ("ulMyReserved", c_ulong),
                ("lMyL2RangeOffset", c_long),
                ("lMyL2CarrierOffset", c_long),
                ("ulMyL2Snr", c_ulong),
                ("ulMyL2SlipCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CMRDATAOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyType0Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyType0Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyType0Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyType0Message_ulMyLength", c_ulong),
                ("clMyType0Message_ulMyVersion", c_ulong),
                ("clMyType0Message_ulMyStationID", c_ulong),
                ("clMyType0Message_ulMessageType", c_ulong),
                ("clMyType0Message_ulMyNumberofSv", c_ulong),
                ("clMyType0Message_ulMyEpochTime", c_ulong),
                ("clMyType0Message_ulMyClockBiasValid", c_ulong),
                ("clMyType0Message_lMyClockOffset", c_long),
                ("clMyType0Message_aclMyCMRBody_arraylength", c_ulong),
                ("clMyType0Message_aclMyCMRBody", CMRDATAOBS_clMyType0Message_aclMyCMRBody*24),
                ]


# noinspection PyTypeChecker
class CMRDATAREF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clType1Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clType1Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clType1Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clType1Message_ulMyLength", c_ulong),
                ("clType1Message_ulMyVersion", c_ulong),
                ("clType1Message_ulMyStationID", c_ulong),
                ("clType1Message_ulMyMessageType", c_ulong),
                ("clType1Message_bMyIsBatteryLow", c_bool),
                ("clType1Message_bMyIsMemLow", c_bool),
                ("clType1Message_ulMyReserved", c_ulong),
                ("clType1Message_bMyIsL2Enabled", c_bool),
                ("clType1Message_ulMyReserved2", c_ulong),
                ("clType1Message_ulMyEpochTime", c_ulong),
                ("clType1Message_ulMyMotionState", c_ulong),
                ("clType1Message_ulMyAntennaNumber", c_ulong),
                ("clMyCMRBody_clType1Message_dMyECEF_X", c_double),
                ("clMyCMRBody_clType1Message_ulMyAntennaH", c_ulong),
                ("clMyCMRBody_clType1Message_dMyECEF_Y", c_double),
                ("clMyCMRBody_clType1Message_ulMyEastOffset", c_ulong),
                ("clMyCMRBody_clType1Message_dMyECEF_Z", c_double),
                ("clMyCMRBody_clType1Message_ulMyNorthOffset", c_ulong),
                ("clMyCMRBody_clType1Message_ulMyPosAccuracy", c_ulong),
                ("clMyCMRBody_clType1Message_ulMyReserved", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCADATA1_clMyRTCAData_Corrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("PseudorangeCorrection", c_double),
                ("IssueofData", c_char),
                ("RangeRateCorrection", c_double),
                ("UDRE", c_float),
                ]


# noinspection PyTypeChecker
class RTCADATA1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAData_ModifiedZCount", c_double),
                ("clMyRTCAData_AEB", c_char),
                ("clMyRTCAData_Corrections_arraylength", c_ulong),
                ("clMyRTCAData_Corrections", RTCADATA1_clMyRTCAData_Corrections*72),
                ]


# noinspection PyTypeChecker
class RTCADATAEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAEPHEM_NovAtelDesignator", c_char),
                ("clMyRTCAEPHEM_ucSubtype", c_char),
                ("clMyRTCAEPHEM_ulMyWeek", c_ulong),
                ("clMyRTCAEPHEM_ulMySeconds", c_ulong),
                ("clMyRTCAEPHEM_ulMyPrn", c_ulong),
                ("clMyRTCAEPHEM_ucMyReserved", c_char),
                ("clMyRTCAEPHEM_aucMyRawData", c_char*90),
                ]


# noinspection PyTypeChecker
class RTCADATAOBS_clMyRTCAOBS_TransmitterData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("L1LockFlag", c_char),
                ("L2LockFlag", c_char),
                ("L1PseudorangeOffset", c_double),
                ("L2PseudorangeOffset", c_double),
                ("L1ADROffset", c_float),
                ("L2ADROffset", c_float),
                ("L2NotEncrypted", c_bool),
                ("Reserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCADATAOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAOBS_NovAtelDesignator", c_char),
                ("clMyRTCAOBS_SubtypeIndicator", c_char),
                ("clMyRTCAOBS_MinimumPseudorange", c_double),
                ("clMyRTCAOBS_Seconds", c_float),
                ("clMyRTCAOBS_Reserved", c_int),
                ("clMyRTCAOBS_TransmitterData_arraylength", c_ulong),
                ("clMyRTCAOBS_TransmitterData", RTCADATAOBS_clMyRTCAOBS_TransmitterData*72),
                ]


# noinspection PyTypeChecker
class RTCADATAREF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAREF_ucMyNovAtelDesignator", c_char),
                ("clMyRTCAREF_ucMySubTypeIndicator", c_char),
                ("clMyRTCAREF_dMyX", c_double),
                ("clMyRTCAREF_dMyY", c_double),
                ("clMyRTCAREF_dMyZ", c_double),
                ("clMyRTCAREF_Reserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1_clMyRTCM1_9_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM1_9_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM1_9_ulMyHealth", c_ulong),
                ("clMyRTCM1_9_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM1_9_aclMyDiffData", RTCMDATA1_clMyRTCM1_9_aclMyDiffData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA15_clMyRTCM15_acMyIonData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyReserved", c_ulong),
                ("ulMyGpsGlonass", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("ulMyCor", c_ulong),
                ("iMyCorrate", c_int),
                ]


# noinspection PyTypeChecker
class RTCMDATA15(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM15_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM15_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM15_ulMyHealth", c_ulong),
                ("clMyRTCM15_acMyIonData_arraylength", c_ulong),
                ("clMyRTCM15_acMyIonData", RTCMDATA15_clMyRTCM15_acMyIonData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA16(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM16_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM16_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM16_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM16_aucMyRTCM16Text_Len", c_ulong),
                ("clMyRTCMBody_clMyRTCM16_aucMyRTCM16Text", c_char*90),
                ]


# noinspection PyTypeChecker
class RTCMDATA1819_clMyRTCM18_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("lMyAdr", c_long),
                ]


# noinspection PyTypeChecker
class RTCMDATA1819_clMyRTCM19_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyPsr", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA1819(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM18_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM18_ulMyHealth", c_ulong),
                ("clMyRTCM18_ulMyFreq", c_ulong),
                ("clMyRTCM18_ulMySpare", c_ulong),
                ("clMyRTCM18_lMyTime", c_long),
                ("clMyRTCM18_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM18_aclMyRTCMBody", RTCMDATA1819_clMyRTCM18_aclMyRTCMBody*15),
                ("clMyRTCMHeader_clMyRTCM19_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM19_ulMyHealth", c_ulong),
                ("clMyRTCM19_ulMyFreq", c_ulong),
                ("clMyRTCM19_ulMySmoothingInterval", c_ulong),
                ("clMyRTCM19_lMyTime", c_long),
                ("clMyRTCM19_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM19_aclMyRTCMBody", RTCMDATA1819_clMyRTCM19_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCMDATA2021_clMyRTCM20_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyInits", c_ulong),
                ("ulIODE", c_ulong),
                ("lPhaseCorr", c_long),
                ]


# noinspection PyTypeChecker
class RTCMDATA2021_clMyRTCM21_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFirstByte_ulMultipleMsg", c_ulong),
                ("clMyFirstByte_ulMyCode", c_ulong),
                ("clMyFirstByte_ulMyConstellation", c_ulong),
                ("clMyFirstByte_ulMySv", c_ulong),
                ("ulMyRateCorrSF", c_ulong),
                ("ulMyDataQual", c_ulong),
                ("ulMyPsrCorrSF", c_ulong),
                ("ulMyMultipath", c_ulong),
                ("ulMyIODE", c_ulong),
                ("lMyPsrCorr", c_long),
                ("lMyPsrCorrRate", c_long),
                ]


# noinspection PyTypeChecker
class RTCMDATA2021(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM20_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM20_ulMyHealth", c_ulong),
                ("clMyRTCM20_ulMyFreq", c_ulong),
                ("clMyRTCM20_ulSpare", c_ulong),
                ("clMyRTCM20_lMyTime", c_long),
                ("clMyRTCM20_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM20_aclMyRTCMBody", RTCMDATA2021_clMyRTCM20_aclMyRTCMBody*15),
                ("clMyRTCMHeader_clMyRTCM21_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM21_ulMyHealth", c_ulong),
                ("clMyRTCM21_ulMyFreq", c_ulong),
                ("clMyRTCM21_ulMySmoothingInterval", c_ulong),
                ("clMyRTCM21_lMyTime", c_long),
                ("clMyRTCM21_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM21_aclMyRTCMBody", RTCMDATA2021_clMyRTCM21_aclMyRTCMBody*15),
                ]


# noinspection PyTypeChecker
class RTCMDATA22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulSpareBits", c_ulong),
                ("bNoHeight", c_bool),
                ("ulAntennaPhaseHeight", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyL2AntDeltaX", c_long),
                ("lMyL2AntDeltaY", c_long),
                ("lMyL2AntDeltaZ", c_long),
                ]


# noinspection PyTypeChecker
class RTCMDATA22(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM22_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaX", c_long),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaY", c_long),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaZ", c_long),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1_arraylength", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1", RTCMDATA22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1*1),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2_arraylength", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2", RTCMDATA22_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2*1),
                ]


# noinspection PyTypeChecker
class RTCMDATA3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM3_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM3_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM3_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCM3_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCM3_dMyECEF_Z", c_double),
                ]


# noinspection PyTypeChecker
class RTCMDATA59_clRTCM59_clMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySv", c_ulong),
                ("ulMyLock", c_ulong),
                ("ulMyPsr", c_ulong),
                ("lMyAdrCor", c_long),
                ]


# noinspection PyTypeChecker
class RTCMDATA59(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clRTCM59_ulMyType", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulRefID", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clRTCM59_ulMyHealth", c_ulong),
                ("clRTCM59_ucMySubType", c_char),
                ("clRTCM59_lMyMinPsr", c_long),
                ("clRTCM59_lTimeOffset", c_long),
                ("clRTCM59_ulSpareBits", c_ulong),
                ("clRTCM59_clMyRTCMBody_arraylength", c_ulong),
                ("clRTCM59_clMyRTCMBody", RTCMDATA59_clRTCM59_clMyRTCMBody*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA9_clMyRTCM9_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA9(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM9_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM9_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM9_ulMyHealth", c_ulong),
                ("clMyRTCM9_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM9_aclMyDiffData", RTCMDATA9_clMyRTCM9_aclMyDiffData*325),
                ]


# noinspection PyTypeChecker
class RAWGPSWORD(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPrn", c_ulong),
                ("ulMyRawWord", c_ulong),
                ]


# noinspection PyTypeChecker
class PDC_VERSIONDATA_aclVersions(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szPSN", c_char*16),
                ("szSoftwareVersion", c_char*16),
                ("szModelName", c_char*16),
                ]


# noinspection PyTypeChecker
class PDC_VERSIONDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclVersions_arraylength", c_ulong),
                ("aclVersions", PDC_VERSIONDATA_aclVersions*20),
                ]


# noinspection PyTypeChecker
class PDC_SATDATA_ChanStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usPrn", c_ushort),
                ("fCNo", c_float),
                ("eMyPSRRangeReject", c_uint),
                ]


# noinspection PyTypeChecker
class PDC_SATDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ChanStatus_arraylength", c_ulong),
                ("ChanStatus", PDC_SATDATA_ChanStatus*325),
                ]


# noinspection PyTypeChecker
class POINTM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPointLogData_fMyDifferentialLag", c_float),
                ("clMyPointLogData_ucMyNumObsUsedInSol", c_char),
                ("clMyPointLogData_ucMyNumHighL1Sats", c_char),
                ("clMyPointLogData_ucMyNumHighL2Sats", c_char),
                ("clMyPointLogData_dMyLatitude", c_double),
                ("clMyPointLogData_dMyLongitude", c_double),
                ("clMyPointLogData_dMyHeight", c_double),
                ("clMyPointLogData_dMyDeltaNorth", c_double),
                ("clMyPointLogData_dMyDeltaEast", c_double),
                ("clMyPointLogData_dMyDeltaUp", c_double),
                ("clMyPointLogData_fMySDev2D", c_float),
                ("clMyPointLogData_fMySDev3D", c_float),
                ("clMyPointLogData_fMySDev1D", c_float),
                ("clMyPointLogData_dMyAzimuth", c_double),
                ("clMyPointLogData_dMyElevation", c_double),
                ("clMyPointLogData_fMySlopeDistance", c_float),
                ("clMyPointLogData_eMyPositionStatus", c_uint),
                ("clMyPointLogData_eMyPositionType", c_uint),
                ("clMyPointLogData_acMyStationID", c_char*4),
                ]


# noinspection PyTypeChecker
class BESTGPSPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PSRDIFFIN_aclMyDiffCorrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteID_eMySystemType", c_uint),
                ("clMySatelliteID_idMyID", satelliteid),
                ("dMyDiffCor", c_double),
                ("dMyDiffCorRate", c_double),
                ]


# noinspection PyTypeChecker
class PSRDIFFIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDGPSType", c_uint),
                ("acMyDiffStationID", c_char*4),
                ("aclMyDiffCorrections_arraylength", c_ulong),
                ("aclMyDiffCorrections", PSRDIFFIN_aclMyDiffCorrections*325),
                ]


# noinspection PyTypeChecker
class PSRDIFFOUT_aclMyDiffCorDatBase(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySVPRN", c_ulong),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ("ulMyIODE", c_ulong),
                ("dMyCor", c_double),
                ("dMyCorRate", c_double),
                ]


# noinspection PyTypeChecker
class PSRDIFFOUT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDiffCorDatBase_arraylength", c_ulong),
                ("aclMyDiffCorDatBase", PSRDIFFOUT_aclMyDiffCorDatBase*32),
                ]


# noinspection PyTypeChecker
class PDPPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PDPVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class PDPXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class TIMESYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulGPSWeek", c_ulong),
                ("ulMilliseconds", c_ulong),
                ("eTimeStatus", c_uint),
                ]


# noinspection PyTypeChecker
class MEMSINSGPS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("dMyLatitude", c_double),
                ("dMyLongitude", c_double),
                ("dMyHeight", c_double),
                ("dMyNorthVelocity", c_double),
                ("dMyEastVelocity", c_double),
                ("dMyUpVelocity", c_double),
                ("dMyElevation", c_double),
                ("dMyRoll", c_double),
                ("dMyAzimuth", c_double),
                ("dMyPitchRate", c_double),
                ("dMyRollRate", c_double),
                ("dMyYawRate", c_double),
                ("dMyLongitudinalAcc", c_double),
                ("dMyLateralAcc", c_double),
                ("dMyVerticalAcc", c_double),
                ]


# noinspection PyTypeChecker
class BESTGPSVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("fFloat", c_float),
                ]


# noinspection PyTypeChecker
class INSPVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSPVAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class RAWIMUSUMS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyGpsWeek", c_ulong),
                ("dMyGpsTime", c_double),
                ("ulMyImuStatus", c_ulong),
                ("ulMyAngBodyX", c_ulong),
                ("ulMyAngBodyY", c_ulong),
                ("ulMyAngBodyZ", c_ulong),
                ("ulMyVelBodyX", c_ulong),
                ("ulMyVelBodyY", c_ulong),
                ("ulMyVelBodyZ", c_ulong),
                ]


# noinspection PyTypeChecker
class APPLICATIONSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulAPIVersion", c_ulong),
                ("bRunning", c_bool),
                ("ulBaseAddress", c_ulong),
                ("ulSize", c_ulong),
                ("szName", c_char*16),
                ("szVersion", c_char*16),
                ("szCompileDate", c_char*12),
                ("szCompileTime", c_char*12),
                ]


# noinspection PyTypeChecker
class GPGGALONG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("ulMyGGAQuality", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ]


# noinspection PyTypeChecker
class INSSTATENVM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eImuType", c_uint),
                ("iMapping", c_int),
                ("adPosEcef", c_double*3),
                ("adAccelBias", c_double*3),
                ("adGyroBias", c_double*3),
                ("mdRlb", c_double*3),
                ("dWheelScale", c_double),
                ("mdP", c_double*66),
                ]


# noinspection PyTypeChecker
class TYPEENUMS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTypeId", c_ulong),
                ("aulMyEnumList_Len", c_ulong),
                ("aulMyEnumList", c_ulong*1000),
                ]


# noinspection PyTypeChecker
class MARK2POS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class MARK2TIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyWeek", c_long),
                ("dMySeconds", c_double),
                ("dMyOffset", c_double),
                ("dMyOffsetStd", c_double),
                ("dMyUTCOffset", c_double),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class TIMEDWHEELDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyWheelDataInfo_usMyTicksPerRev", c_ushort),
                ("clMyWheelDataInfo_usMyWheelVelocity", c_ushort),
                ("clMyWheelDataInfo_fMyWheelVelocity", c_float),
                ("clMyWheelDataInfo_ulMyReserved1", c_ulong),
                ("clMyWheelDataInfo_ulMyOptions", c_ulong),
                ("clMyWheelDataInfo_lMyCumulativeTicksPerSecond", c_long),
                ]


# noinspection PyTypeChecker
class RANGEGPSL1_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySvPrn", c_ushort),
                ("usMySvFreq", c_ushort),
                ("dMyPsr", c_double),
                ("fMySDPsr", c_float),
                ("dMyAdr", c_double),
                ("fMySDAdr", c_float),
                ("fMyDop", c_float),
                ("fMyUserCNo", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class RANGEGPSL1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyObs_arraylength", c_ulong),
                ("aclMyObs", RANGEGPSL1_aclMyObs*325),
                ]


# noinspection PyTypeChecker
class CBITHINT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyHint", c_uint),
                ("ulMyParam1", c_ulong),
                ("ulMyParam2", c_ulong),
                ("ulMyParam3", c_ulong),
                ("ulMyHintString", c_char*100),
                ]


# noinspection PyTypeChecker
class DEBUGETHERRSRC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyInUseRequestors", c_ulong),
                ("ulMyHighWaterMarkRequestors", c_ulong),
                ("ulMyMaxRequestors", c_ulong),
                ("ulMyInUseRateRequests", c_ulong),
                ("ulMyHighWaterMarkRateRequests", c_ulong),
                ("ulMyMaxRateRequests", c_ulong),
                ]


# noinspection PyTypeChecker
class TIMEDMAGDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMagId", c_ushort),
                ("usMagStatus", c_ushort),
                ("sXMag", c_short),
                ("sYMag", c_short),
                ("sZMag", c_short),
                ]


# noinspection PyTypeChecker
class WHEELSIZE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyWheelScale", c_double),
                ("dMyWheelCircumference", c_double),
                ("dMyWheelVariance", c_double),
                ]


# noinspection PyTypeChecker
class SATVISSYS_aclMySatVisList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("bMyPosVelValid", c_bool),
                ("usMyPrn", c_ushort),
                ("usMyFreq", c_ushort),
                ("ulMySatHealth", c_ulong),
                ("dMyElevation", c_double),
                ("dMyAzimuth", c_double),
                ("dMyTrueDoppler", c_double),
                ("dMyApparentDoppler", c_double),
                ("eMySystemType", c_uint),
                ("eMySystemVariant", c_uint),
                ]


# noinspection PyTypeChecker
class SATVISSYS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("bMyIsSatVisValid", c_bool),
                ("bMyWasGPSAlmanacUsed", c_bool),
                ("aclMySatVisList_arraylength", c_ulong),
                ("aclMySatVisList", SATVISSYS_aclMySatVisList*318),
                ]


# noinspection PyTypeChecker
class RTCMDATA59FKP_clRTCM59FKP_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyIOD", c_ulong),
                ("ulMyReserve", c_ulong),
                ("ulMySL0", c_ulong),
                ("ulMySLI", c_ulong),
                ("ulMyN0", c_long),
                ("ulMyNI", c_long),
                ("ulMyE0", c_long),
                ("ulMyEI", c_long),
                ]


# noinspection PyTypeChecker
class RTCMDATA59FKP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clRTCM59FKP_ulMyType", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulRefID", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMyHealth", c_ulong),
                ("clRTCM59FKP_ulInstitutionId1", c_ulong),
                ("clRTCM59FKP_ulInstitutionId2", c_ulong),
                ("clRTCM59FKP_ulInstitutionId3", c_ulong),
                ("clRTCM59FKP_ulSubID", c_ulong),
                ("clRTCM59FKP_ulReserve", c_ulong),
                ("clRTCM59FKP_ulDataSetNumber", c_ulong),
                ("clRTCM59FKP_ulSatIdBitMask", c_ulong),
                ("clRTCM59FKP_aclMyRTCMBody_arraylength", c_ulong),
                ("clRTCM59FKP_aclMyRTCMBody", RTCMDATA59FKP_clRTCM59FKP_aclMyRTCMBody*325),
                ]


# noinspection PyTypeChecker
class RTCM59FKPIN_clMyRTCM59FKP_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyIOD", c_ulong),
                ("ulMyReserve", c_ulong),
                ("ulMySL0", c_ulong),
                ("ulMySLI", c_ulong),
                ("ulMyN0", c_long),
                ("ulMyNI", c_long),
                ("ulMyE0", c_long),
                ("ulMyEI", c_long),
                ]


# noinspection PyTypeChecker
class RTCM59FKPIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM59FKP_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59FKP_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59FKP_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59FKP_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59FKP_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM59FKP_ulMyHealth", c_ulong),
                ("clMyRTCM59FKP_ulInstitutionId1", c_ulong),
                ("clMyRTCM59FKP_ulInstitutionId2", c_ulong),
                ("clMyRTCM59FKP_ulInstitutionId3", c_ulong),
                ("clMyRTCM59FKP_ulSubID", c_ulong),
                ("clMyRTCM59FKP_ulReserve", c_ulong),
                ("clMyRTCM59FKP_ulDataSetNumber", c_ulong),
                ("clMyRTCM59FKP_ulSatIdBitMask", c_ulong),
                ("clMyRTCM59FKP_aclMyRTCMBody_arraylength", c_ulong),
                ("clMyRTCM59FKP_aclMyRTCMBody", RTCM59FKPIN_clMyRTCM59FKP_aclMyRTCMBody*325),
                ]


# noinspection PyTypeChecker
class RTCM59FKP_clRTCM59FKP_aclMyRTCMBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyIOD", c_ulong),
                ("ulMyReserve", c_ulong),
                ("ulMySL0", c_ulong),
                ("ulMySLI", c_ulong),
                ("ulMyN0", c_long),
                ("ulMyNI", c_long),
                ("ulMyE0", c_long),
                ("ulMyEI", c_long),
                ]


# noinspection PyTypeChecker
class RTCM59FKP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clRTCM59FKP_ulMyType", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulRefID", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clRTCM59FKP_ulMyHealth", c_ulong),
                ("clRTCM59FKP_ulInstitutionId1", c_ulong),
                ("clRTCM59FKP_ulInstitutionId2", c_ulong),
                ("clRTCM59FKP_ulInstitutionId3", c_ulong),
                ("clRTCM59FKP_ulSubID", c_ulong),
                ("clRTCM59FKP_ulReserve", c_ulong),
                ("clRTCM59FKP_ulDataSetNumber", c_ulong),
                ("clRTCM59FKP_ulSatIdBitMask", c_ulong),
                ("clRTCM59FKP_aclMyRTCMBody_arraylength", c_ulong),
                ("clRTCM59FKP_aclMyRTCMBody", RTCM59FKP_clRTCM59FKP_aclMyRTCMBody*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA23(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM23_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMyReserved1", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMyAR", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMySF", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaDescription_Len", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaDescription", c_char*31),
                ("clMyRTCMREFData_clMyRTCM23_ulMySetupID", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMyReserved2", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class RTCMDATA24_clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyAntHgt", c_ulong),
                ("ulMyAntRsr", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA24(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM24_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCM24_ulMyReserved1", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCM24_ulMyReserved2", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_dMyECEF_Z", c_double),
                ("clMyRTCMREFData_clMyRTCM24_ulMySystemIndicator", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_ulMyAntennaHtFlag", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf_arraylength", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf", RTCMDATA24_clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf*1),
                ]


# noinspection PyTypeChecker
class RTCM23(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM23_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM23_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMyReserved1", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMyAR", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMySF", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaDescription_Len", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaDescription", c_char*31),
                ("clMyRTCMREFData_clMyRTCM23_ulMySetupID", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_ulMyReserved2", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMREFData_clMyRTCM23_szMyAntennaSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class RTCM23IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMREF_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_ulMyReserved1", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_ulMyAR", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_ulMySF", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_szMyAntennaDescription_Len", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_szMyAntennaDescription", c_char*31),
                ("clMyRTCMREFData_clMyRTCMREF_ulMySetupID", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_ulMyReserved2", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_szMyAntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_szMyAntennaSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class RTCM24_clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyAntHgt", c_ulong),
                ("ulMyAntRsr", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM24(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM24_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM24_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCM24_ulMyReserved1", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCM24_ulMyReserved2", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_dMyECEF_Z", c_double),
                ("clMyRTCMREFData_clMyRTCM24_ulMySystemIndicator", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_ulMyAntennaHtFlag", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf_arraylength", c_ulong),
                ("clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf", RTCM24_clMyRTCMREFData_clMyRTCM24_clMyAntHgtInf*1),
                ]


# noinspection PyTypeChecker
class RTCM24IN_clMyRTCMREFData_clMyRTCMREF_clMyAntHgtInf(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyAntHgt", c_ulong),
                ("ulMyAntRsr", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM24IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMREF_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCMREF_ulMyReserved1", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCMREF_ulMyReserved2", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_Z", c_double),
                ("clMyRTCMREFData_clMyRTCMREF_ulMySystemIndicator", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_ulMyAntennaHtFlag", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_clMyAntHgtInf_arraylength", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_clMyAntHgtInf", RTCM24IN_clMyRTCMREFData_clMyRTCMREF_clMyAntHgtInf*1),
                ]


# noinspection PyTypeChecker
class RAWIMUIFCARDPACKET(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyIMUIFCardHeader_ucMyIMUIFCardMsgID", c_char),
                ("clMyIMUIFCardBody_aucMyData", c_char*64),
                ("usMyIMUIFCardCksum", c_ushort),
                ]


# noinspection PyTypeChecker
class IMUCARDDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyDebugBuffer", c_char*64),
                ]


# noinspection PyTypeChecker
class IMUCARDSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySDLCCntRcvCRCFrameOK", c_ulong),
                ("ulMySDLCCntRcvInertialMsg", c_ulong),
                ("usMySDLCCntRcvAbortError", c_ushort),
                ("usMySDLCCntRcvCRCError", c_ushort),
                ("usMySDLCCntRcvBufferOverRun", c_ushort),
                ("usMySDLCReserved1", c_ushort),
                ("usMySDLCReserved2", c_ushort),
                ("usMySDLCReserved3", c_ushort),
                ("usMyUARTRcvBufferOverRun", c_ushort),
                ("usMyUARTRcvOverRunError", c_ushort),
                ("usMyUARTRcvFrameError", c_ushort),
                ("usMyUARTRcvParityError", c_ushort),
                ("usMyUARTRcvArbitrationError", c_ushort),
                ("usMyUARTReserved1", c_ushort),
                ("ulMyTIMERTmrOutofBoundsShort", c_ulong),
                ("ulMyTIMERTmrOutofBoundsLong", c_ulong),
                ("ulMyTIMERTmrReserved", c_ulong),
                ("ulMyNONINTError", c_ulong),
                ("ulMyNONINTRcvMsgCRCError", c_ulong),
                ("ulMyNONINTRcvIdleTime", c_ulong),
                ("ulMyNONINTReserved4", c_ulong),
                ("ulMyNONINTReserved5", c_ulong),
                ]


# noinspection PyTypeChecker
class IMUCARDVERSION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyBuildDate", c_char*12),
                ("acMyBuildTime", c_char*12),
                ("acMyVersion", c_char*12),
                ("aucMyReserved", c_char*28),
                ]


# noinspection PyTypeChecker
class BESTLEVERARM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLeverArm_adMyInput", c_double*3),
                ("clMyLeverArm_adMyInputStdev", c_double*3),
                ("iMyMapping", c_int),
                ]


# noinspection PyTypeChecker
class SOLVEDLEVERARM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("adMyRgib", c_double*3),
                ("adMyRgib_Accuracy", c_double*3),
                ]


# noinspection PyTypeChecker
class BSLNXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyECEFBaseline_dMyX", c_double),
                ("clMyECEFBaseline_dMyY", c_double),
                ("clMyECEFBaseline_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class DEBUGETHERRSRC2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyInUseRequestors", c_ulong),
                ("ulMyHighWaterMarkRequestors", c_ulong),
                ("ulMyMaxRequestors", c_ulong),
                ("ulMyInUseRateRequests", c_ulong),
                ("ulMyHighWaterMarkRateRequests", c_ulong),
                ("ulMyMaxRateRequests", c_ulong),
                ("ulMyInUseTaskHandles", c_ulong),
                ("ulMyHighWaterMarkTaskHandles", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGETHERS2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyEtherName", c_char*51),
                ("ulMyEtherNum", c_ulong),
                ("ulMyEtherSiblingNum", c_ulong),
                ("ulMyNumPackets", c_ulong),
                ("ulMyHighWaterPackets", c_ulong),
                ("ulMyPacketCap", c_ulong),
                ("ulMyNumRequestors", c_ulong),
                ("bMyIsCommMsgQTaken", c_bool),
                ("ulMyCommMsgQID", c_ulong),
                ("ulMyProviderTaskID", c_ulong),
                ]


# noinspection PyTypeChecker
class WAAS32(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class WAAS33(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class WAAS34(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class WAAS35(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class WAAS45(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFirstHalf_ulMyPRNMaskNumber", c_ulong),
                ("clMyFirstHalf_ulMyIODE", c_ulong),
                ("clMyFirstHalf_lMyDX", c_long),
                ("clMyFirstHalf_lMyDY", c_long),
                ("clMyFirstHalf_lMyDZ", c_long),
                ("clMyFirstHalf_lMyDDX", c_long),
                ("clMyFirstHalf_lMyDDY", c_long),
                ("clMyFirstHalf_lMyDDZ", c_long),
                ("clMyFirstHalf_lMyDAF0", c_long),
                ("clMyFirstHalf_ulMyTOD", c_ulong),
                ("clMySecondHalf_ulMyPRNMaskNumber", c_ulong),
                ("clMySecondHalf_ulMyIODE", c_ulong),
                ("clMySecondHalf_lMyDX", c_long),
                ("clMySecondHalf_lMyDY", c_long),
                ("clMySecondHalf_lMyDZ", c_long),
                ("clMySecondHalf_lMyDDX", c_long),
                ("clMySecondHalf_lMyDDY", c_long),
                ("clMySecondHalf_lMyDDZ", c_long),
                ("clMySecondHalf_lMyDAF0", c_long),
                ("clMySecondHalf_ulMyTOD", c_ulong),
                ("ulMyIODP", c_ulong),
                ]


# noinspection PyTypeChecker
class FKPCORRECTIONS_aMyFKPCorrection(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyNonDispersiveErrorL1", c_double),
                ("dMyDispersiveErrorL1", c_double),
                ]


# noinspection PyTypeChecker
class FKPCORRECTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyFKPPRNMask", c_ulong),
                ("aMyFKPCorrection_arraylength", c_ulong),
                ("aMyFKPCorrection", FKPCORRECTIONS_aMyFKPCorrection*325),
                ]


# noinspection PyTypeChecker
class CMRPLUSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyCMRPlusData_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyCMRPlusData_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyCMRPlusData_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyCMRPlusData_ulMyLength", c_ulong),
                ("clMyCMRPlusData_ulMyStationID", c_ulong),
                ("clMyCMRPlusData_ulMyPage", c_ulong),
                ("clMyCMRPlusData_ulMyNumPages", c_ulong),
                ("clMyCMRPlusData_aucMyData_Len", c_ulong),
                ("clMyCMRPlusData_aucMyData", c_char*7),
                ]


# noinspection PyTypeChecker
class MMTRAWDATA_aclMyBins(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyI", c_long),
                ("lMyQ", c_long),
                ]


# noinspection PyTypeChecker
class MMTRAWDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("ulMyPrn", c_ulong),
                ("aclMyBins_arraylength", c_ulong),
                ("aclMyBins", MMTRAWDATA_aclMyBins*18),
                ]


# noinspection PyTypeChecker
class CMRPLUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyCMRPlusData_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyCMRPlusData_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyCMRPlusData_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyCMRPlusData_ulMyLength", c_ulong),
                ("clMyCMRPlusData_ulMyStationID", c_ulong),
                ("clMyCMRPlusData_ulMyPage", c_ulong),
                ("clMyCMRPlusData_ulMyNumPages", c_ulong),
                ("clMyCMRPlusData_aucMyData_Len", c_ulong),
                ("clMyCMRPlusData_aucMyData", c_char*7),
                ]


# noinspection PyTypeChecker
class GLOALMANAC_aclMySatAlmData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRefTime_ulMyWeeks", c_ulong),
                ("clMyRefTime_ulMyMilliseconds", c_ulong),
                ("ucMySlot", c_char),
                ("cMyFrequency", c_char),
                ("ucMySatType", c_char),
                ("ucMyHealth", c_char),
                ("dMyTLambdaN", c_double),
                ("dMyLambdaN", c_double),
                ("dMyDeltaI", c_double),
                ("dMyEcc", c_double),
                ("dMyArgPerig", c_double),
                ("dMyDeltaT", c_double),
                ("dMyDeltaTD", c_double),
                ("dMyTau", c_double),
                ]


# noinspection PyTypeChecker
class GLOALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySatAlmData_arraylength", c_ulong),
                ("aclMySatAlmData", GLOALMANAC_aclMySatAlmData*24),
                ]


# noinspection PyTypeChecker
class GLOCLOCK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNominalOffset", c_ulong),
                ("dMyResidualOffset", c_double),
                ("dMyResidualOffsetVar", c_double),
                ("clMyClockParams_ucMySatType", c_char),
                ("clMyClockParams_ucMyN4", c_char),
                ("clMyClockParams_dMyTauGPS", c_double),
                ("clMyClockParams_usMyNA", c_ushort),
                ("clMyClockParams_dMyTauC", c_double),
                ("clMyClockParams_dMyB1", c_double),
                ("clMyClockParams_dMyB2", c_double),
                ("clMyClockParams_ucMyKP", c_char),
                ]


# noinspection PyTypeChecker
class GLORAWALM_aclMyStrings(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyString", c_char*11),
                ("ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class GLORAWALM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyStrings_arraylength", c_ulong),
                ("aclMyStrings", GLORAWALM_aclMyStrings*54),
                ]


# noinspection PyTypeChecker
class GLORAWFRAME_aclMyRawString(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyString", c_char*11),
                ("ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class GLORAWFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyFrameNumber", c_ulong),
                ("usMySloto", c_ushort),
                ("usMyFreqo", c_ushort),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("ulMyFrameDecoderNumber", c_ulong),
                ("ulMySignalChannelNumber", c_ulong),
                ("aclMyRawString_arraylength", c_ulong),
                ("aclMyRawString", GLORAWFRAME_aclMyRawString*15),
                ]


# noinspection PyTypeChecker
class GLORAWSTRING(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySlot", c_char),
                ("cMyFreq", c_char),
                ("clMyStringBuffer_aucMyString", c_char*11),
                ("clMyStringBuffer_ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class GLOEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySloto", c_ushort),
                ("usMyFreqo", c_ushort),
                ("clMyEphemParams_ucMySatType", c_char),
                ("clMyEphemParams_ucMyFalseIOD", c_char),
                ("clMyEphemParams_usMyEphemWeek", c_ushort),
                ("clMyEphemParams_ulMyEphemTime", c_ulong),
                ("clMyEphemParams_ulMyTimeOffset", c_ulong),
                ("clMyEphemParams_usMyNt", c_ushort),
                ("clMyEphemParams_ucMyReserved", c_char),
                ("clMyEphemParams_ucMyReserved", c_char),
                ("clMyEphemParams_ulMyIssue", c_ulong),
                ("clMyEphemParams_ulMyBroadcastHealth", c_ulong),
                ("clMyEphemParams_dMyPosX", c_double),
                ("clMyEphemParams_dMyPosY", c_double),
                ("clMyEphemParams_dMyPosZ", c_double),
                ("clMyEphemParams_dMyVelX", c_double),
                ("clMyEphemParams_dMyVelY", c_double),
                ("clMyEphemParams_dMyVelZ", c_double),
                ("clMyEphemParams_dMyLSAccX", c_double),
                ("clMyEphemParams_dMyLSAccY", c_double),
                ("clMyEphemParams_dMyLSAccZ", c_double),
                ("clMyEphemParams_dMyTau", c_double),
                ("clMyEphemParams_dMyDeltaTau", c_double),
                ("clMyEphemParams_dMyGamma", c_double),
                ("clMyEphemParams_ulMyTk", c_ulong),
                ("clMyEphemParams_ulMyP", c_ulong),
                ("clMyEphemParams_ulMyFt", c_ulong),
                ("clMyEphemParams_ulMyAge", c_ulong),
                ("clMyEphemParams_ulMyFlags", c_ulong),
                ]


# noinspection PyTypeChecker
class BESTUTM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("ulMyZoneNumber", c_ulong),
                ("ulMyZoneLetter", c_ulong),
                ("dMyNorthing", c_double),
                ("dMyEasting", c_double),
                ("dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class VISIONCALDATA_clMyMMTData_aclMyBins(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyI", c_long),
                ("lMyQ", c_long),
                ("lMyCount", c_long),
                ("lMyEndpoint", c_long),
                ]


# noinspection PyTypeChecker
class VISIONCALDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPrn", c_ulong),
                ("clMyMMTData_aclMyBins_arraylength", c_ulong),
                ("clMyMMTData_aclMyBins", VISIONCALDATA_clMyMMTData_aclMyBins*18),
                ("clMyRemainderBin_clMyMMTData_lMyI", c_long),
                ("clMyRemainderBin_clMyMMTData_lMyQ", c_long),
                ("clMyRemainderBin_clMyMMTData_lMyCount", c_long),
                ("clMyRemainderBin_clMyMMTData_lMyEndpoint", c_long),
                ]


# noinspection PyTypeChecker
class RAWLBANDFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyServiceID", c_ushort),
                ("usMyReserved", c_ushort),
                ("aucData_Len", c_ulong),
                ("aucData", c_char*512),
                ]


# noinspection PyTypeChecker
class RAWLBANDPACKET(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucData_Len", c_ulong),
                ("aucData", c_char*512),
                ]


# noinspection PyTypeChecker
class RAWNAVMSGDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyReceiveTime_ulMyPicoseconds", c_ulong),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_bMyIsNegative", c_bool),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("clMyReceiveTime_eMyTimeStatus", c_uint),
                ("ulMyNumRawBits", c_ulong),
                ("aucMyRawBits", c_char*4),
                ("aucMyBadPowerBitIndex", c_char*4),
                ("ulMySignalChannelNumber", c_ulong),
                ("ulMyBitPeriodUS", c_ulong),
                ("aucMyPhaseLocked", c_char*4),
                ]


# noinspection PyTypeChecker
class GROUPCOMCONFIG_aclMyComConfigs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("ulMyStatus", c_ulong),
                ("ulMyBaud", c_ulong),
                ("eMyParity", c_uint),
                ("ulMyDataBits", c_ulong),
                ("ulMyStopBits", c_ulong),
                ("eMyHandshake", c_uint),
                ("eMyEcho", c_uint),
                ("eMyBreaks", c_uint),
                ("eMyRXType", c_uint),
                ("eMyTXType", c_uint),
                ("eMyResponses", c_uint),
                ("eMyComVoutAction", c_uint),
                ("ulMyReserved", c_ulong),
                ]


# noinspection PyTypeChecker
class GROUPCOMCONFIG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyGroupName", c_char*12),
                ("aclMyComConfigs_arraylength", c_ulong),
                ("aclMyComConfigs", GROUPCOMCONFIG_aclMyComConfigs*53),
                ]


# noinspection PyTypeChecker
class INSUTM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulWeek", c_ulong),
                ("dSeconds", c_double),
                ("ulMyZoneNumber", c_ulong),
                ("ulMyZoneLetter", c_ulong),
                ("dMyNorthing", c_double),
                ("dMyEasting", c_double),
                ("dMyHeight", c_double),
                ("eStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSUPDATE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPosType", c_uint),
                ("iMyNumPSR", c_int),
                ("iMyNumPhase", c_int),
                ("iMyNumDOP", c_int),
                ("bMyZuptEpoch", c_bool),
                ("eMyWheelStatus", c_uint),
                ("eMyHeadingUpdateStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSRB(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyRB", c_double),
                ("dMyRBR", c_double),
                ("dMyRBstd", c_double),
                ("dMyRBRstd", c_double),
                ("bMyConstChg", c_bool),
                ("eMyPositionStatus", c_uint),
                ]


# noinspection PyTypeChecker
class VISIONREFFUNC_aclMyRefPoints(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyI", c_float),
                ("fMyQ", c_float),
                ]


# noinspection PyTypeChecker
class VISIONREFFUNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyRefName", c_char*12),
                ("ulMyRefStatus", c_ulong),
                ("aclMyRefPoints_arraylength", c_ulong),
                ("aclMyRefPoints", VISIONREFFUNC_aclMyRefPoints*301),
                ]


# noinspection PyTypeChecker
class VISIONSOL_clMyMMTSolvedParams(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyChannel", c_ushort),
                ("usMyPrn", c_ushort),
                ("bMyHaveMP", c_bool),
                ("fMyTau1", c_float),
                ("fMyPhi1", c_float),
                ("fMyAmp1", c_float),
                ("fMyTau2", c_float),
                ("fMyPhi2", c_float),
                ("fMyAmp2", c_float),
                ("fMyLKF", c_float),
                ]


# noinspection PyTypeChecker
class VISIONSOL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyMMTSolvedParams_arraylength", c_ulong),
                ("clMyMMTSolvedParams", VISIONSOL_clMyMMTSolvedParams*325),
                ]


# noinspection PyTypeChecker
class RTCM1005IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_ITRFRealizationYear", c_char),
                ("clMyRTCMV3REF_GPSIndicator", c_char),
                ("clMyRTCMV3REF_GLONASSIndicator", c_char),
                ("clMyRTCMV3REF_GalileoIndicator", c_char),
                ("clMyRTCMV3REF_ReferenceStationIndicator", c_char),
                ("clMyRTCMV3REF_ECEFX", c_double),
                ("clMyRTCMV3REF_SingleReceiverOscIndicator", c_char),
                ("clMyRTCMV3REF_Reserved", c_char),
                ("clMyRTCMV3REF_ECEFY", c_double),
                ("clMyRTCMV3REF_QuarterCycleIndicator", c_char),
                ("clMyRTCMV3REF_ECEFZ", c_double),
                ]


# noinspection PyTypeChecker
class RTCM1005(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_ITRFRealizationYear", c_char),
                ("clMyRTCMV3REF_GPSIndicator", c_char),
                ("clMyRTCMV3REF_GLONASSIndicator", c_char),
                ("clMyRTCMV3REF_GalileoIndicator", c_char),
                ("clMyRTCMV3REF_ReferenceStationIndicator", c_char),
                ("clMyRTCMV3REF_ECEFX", c_double),
                ("clMyRTCMV3REF_SingleReceiverOscIndicator", c_char),
                ("clMyRTCMV3REF_Reserved", c_char),
                ("clMyRTCMV3REF_ECEFY", c_double),
                ("clMyRTCMV3REF_QuarterCycleIndicator", c_char),
                ("clMyRTCMV3REF_ECEFZ", c_double),
                ]


# noinspection PyTypeChecker
class RTCM1006IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_ITRFRealizationYear", c_char),
                ("clMyRTCMV3REF_GPSIndicator", c_char),
                ("clMyRTCMV3REF_GLONASSIndicator", c_char),
                ("clMyRTCMV3REF_GalileoIndicator", c_char),
                ("clMyRTCMV3REF_ReferenceStationIndicator", c_char),
                ("clMyRTCMV3REF_ECEFX", c_double),
                ("clMyRTCMV3REF_SingleReceiverOscIndicator", c_char),
                ("clMyRTCMV3REF_Reserved", c_char),
                ("clMyRTCMV3REF_ECEFY", c_double),
                ("clMyRTCMV3REF_QuarterCycleIndicator", c_char),
                ("clMyRTCMV3REF_ECEFZ", c_double),
                ("clMyRTCMV3REF_AntennaHeight", c_ushort),
                ]


# noinspection PyTypeChecker
class RTCM1006(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_ITRFRealizationYear", c_char),
                ("clMyRTCMV3REF_GPSIndicator", c_char),
                ("clMyRTCMV3REF_GLONASSIndicator", c_char),
                ("clMyRTCMV3REF_GalileoIndicator", c_char),
                ("clMyRTCMV3REF_ReferenceStationIndicator", c_char),
                ("clMyRTCMV3REF_ECEFX", c_double),
                ("clMyRTCMV3REF_SingleReceiverOscIndicator", c_char),
                ("clMyRTCMV3REF_Reserved", c_char),
                ("clMyRTCMV3REF_ECEFY", c_double),
                ("clMyRTCMV3REF_QuarterCycleIndicator", c_char),
                ("clMyRTCMV3REF_ECEFZ", c_double),
                ("clMyRTCMV3REF_AntennaHeight", c_ushort),
                ]


# noinspection PyTypeChecker
class RTCM1004IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ("L2CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1004IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1004IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1004_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ("L2CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1004(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1004_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1001IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1001IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1001IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1001_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1001(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1001_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1002IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1002IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1002IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1002_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1002(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1002_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1003IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1003IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1003IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1003_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1003(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1003_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1001_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1001(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1001_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1002_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1002(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1002_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1003_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1003(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1003_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1004_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ("L2CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1004(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1004_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1005(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_ITRFRealizationYear", c_char),
                ("clMyRTCMV3REF_GPSIndicator", c_char),
                ("clMyRTCMV3REF_GLONASSIndicator", c_char),
                ("clMyRTCMV3REF_GalileoIndicator", c_char),
                ("clMyRTCMV3REF_ReferenceStationIndicator", c_char),
                ("clMyRTCMV3REF_ECEFX", c_double),
                ("clMyRTCMV3REF_SingleReceiverOscIndicator", c_char),
                ("clMyRTCMV3REF_Reserved", c_char),
                ("clMyRTCMV3REF_ECEFY", c_double),
                ("clMyRTCMV3REF_QuarterCycleIndicator", c_char),
                ("clMyRTCMV3REF_ECEFZ", c_double),
                ]


# noinspection PyTypeChecker
class RTCMDATA1006(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_ITRFRealizationYear", c_char),
                ("clMyRTCMV3REF_GPSIndicator", c_char),
                ("clMyRTCMV3REF_GLONASSIndicator", c_char),
                ("clMyRTCMV3REF_GalileoIndicator", c_char),
                ("clMyRTCMV3REF_ReferenceStationIndicator", c_char),
                ("clMyRTCMV3REF_ECEFX", c_double),
                ("clMyRTCMV3REF_SingleReceiverOscIndicator", c_char),
                ("clMyRTCMV3REF_Reserved", c_char),
                ("clMyRTCMV3REF_ECEFY", c_double),
                ("clMyRTCMV3REF_QuarterCycleIndicator", c_char),
                ("clMyRTCMV3REF_ECEFZ", c_double),
                ("clMyRTCMV3REF_AntennaHeight", c_ushort),
                ]


# noinspection PyTypeChecker
class GLORAWEPHEM_aclGloRawEphem(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyString", c_char*11),
                ("ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class GLORAWEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySloto", c_ushort),
                ("usMyFreqo", c_ushort),
                ("ulMySignalChannelNumber", c_ulong),
                ("clMyReferenceTime_ulMyWeeks", c_ulong),
                ("clMyReferenceTime_ulMyMilliseconds", c_ulong),
                ("aclGloRawEphem_arraylength", c_ulong),
                ("aclGloRawEphem", GLORAWEPHEM_aclGloRawEphem*4),
                ]


# noinspection PyTypeChecker
class PRXSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aulMyTemperature", c_ulong*8),
                ("usMyVersion", c_ushort),
                ("usMyFlags", c_ushort),
                ("fMyHighWaterTemp", c_float),
                ("ulMyWeeks", c_ulong),
                ("ulMyMilliseconds", c_ulong),
                ("ulMyBootCount", c_ulong),
                ("ulMyFResetCount", c_ulong),
                ("eMyFResetTarget", c_uint),
                ("aulMyFiller", c_ulong*25),
                ]


# noinspection PyTypeChecker
class AUDIOCFGDEF_ulMyNumEvents(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eAudioEvent", c_uint),
                ("ulMyVolume", c_ulong),
                ]


# noinspection PyTypeChecker
class AUDIOCFGDEF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyAudioBlock", c_char*8),
                ("usMyAudioIndex", c_ushort),
                ("usMyReserved", c_ushort),
                ("ulMyNumEvents_arraylength", c_ulong),
                ("ulMyNumEvents", AUDIOCFGDEF_ulMyNumEvents*14),
                ]


# noinspection PyTypeChecker
class EXTLEVELS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyGPSTemperature", c_float),
                ("fMyAntennaCurrent", c_float),
                ("fMyCoreVoltage", c_float),
                ("fMySupplyVoltage", c_float),
                ("fMyRFVoltage", c_float),
                ("fMyIntLNAVoltage", c_float),
                ("fMyLNAVoltage", c_float),
                ("ulMyBattLife", c_ulong),
                ("fMyBattVolt", c_float),
                ("fMyBattTemp", c_float),
                ("ulMyDiskSpace", c_ulong),
                ("fMyReserved1", c_float),
                ("fMyReserved2", c_float),
                ("fMyReserved3", c_float),
                ("fMyReserved4", c_float),
                ("fMyReserved5", c_float),
                ]


# noinspection PyTypeChecker
class PWRSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPortPowerStatus", c_ulong),
                ("ulMyRxStatusWord2", c_ulong),
                ("ulMyRxStatusWord3", c_ulong),
                ("fMyBattVolt", c_float),
                ("fMyChargeVolt", c_float),
                ("fMyExtVolt", c_float),
                ("ulMyBattLife", c_ulong),
                ("ulMyChargeTime", c_ulong),
                ("ulMyRelativeSOC", c_ulong),
                ("ulMyAbsoluteSOC", c_ulong),
                ("ulMyReserved1", c_ulong),
                ("ulMyReserved2", c_ulong),
                ("ulMyReserved3", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCAOBS2_clMyRTCAObs2_Transmitter2Data(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("L1LockTime", c_char),
                ("L1PsrOffset", c_double),
                ("L1ADROffset", c_double),
                ("FreqAvail", c_char),
                ("CodeType", c_char),
                ("Reserved", c_char),
                ("L2LockTime", c_char),
                ("L2PsrOffset", c_double),
                ("L2ADROffset", c_double),
                ("CodeType2", c_char),
                ("Reserved2", c_char),
                ]


# noinspection PyTypeChecker
class RTCAOBS2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAObs2_NovAtelDesignator", c_char),
                ("clMyRTCAObs2_SubtypeIndicator", c_char),
                ("clMyRTCAObs2_ReceiverTimeBias", c_double),
                ("clMyRTCAObs2_Seconds", c_float),
                ("clMyRTCAObs2_GloCalibrationQual", c_char),
                ("clMyRTCAObs2_Reserved", c_int),
                ("clMyRTCAObs2_Transmitter2Data_arraylength", c_ulong),
                ("clMyRTCAObs2_Transmitter2Data", RTCAOBS2_clMyRTCAObs2_Transmitter2Data*72),
                ]


# noinspection PyTypeChecker
class RTCAOBS2IN_clMyRTCAOBS_Transmitter2Data(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("L1LockTime", c_char),
                ("L1PsrOffset", c_double),
                ("L1ADROffset", c_double),
                ("FreqAvail", c_char),
                ("CodeType", c_char),
                ("Reserved", c_char),
                ("L2LockTime", c_char),
                ("L2PsrOffset", c_double),
                ("L2ADROffset", c_double),
                ("CodeType2", c_char),
                ("Reserved2", c_char),
                ]


# noinspection PyTypeChecker
class RTCAOBS2IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clHeader_clMyRTCAOBS_ulMessageIdentifier", c_ulong),
                ("clHeader_clMyRTCAOBS_ulRefStation", c_ulong),
                ("clHeader_clMyRTCAOBS_ulMessageType", c_ulong),
                ("clHeader_clMyRTCAOBS_ulReserved", c_ulong),
                ("clHeader_clMyRTCAOBS_ulMessageLength", c_ulong),
                ("clMyRTCAOBS_NovAtelDesignator", c_char),
                ("clMyRTCAOBS_SubtypeIndicator", c_char),
                ("clMyRTCAOBS_ReceiverTimeBias", c_double),
                ("clMyRTCAOBS_Seconds", c_float),
                ("clMyRTCAOBS_GloCalibrationQual", c_char),
                ("clMyRTCAOBS_Reserved", c_int),
                ("clMyRTCAOBS_Transmitter2Data_arraylength", c_ulong),
                ("clMyRTCAOBS_Transmitter2Data", RTCAOBS2IN_clMyRTCAOBS_Transmitter2Data*72),
                ]


# noinspection PyTypeChecker
class RTCA2IN_clMyRTCAData_Corrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("PseudorangeCorrection", c_double),
                ("IssueofData", c_char),
                ("RangeRateCorrection", c_double),
                ("UDRE", c_float),
                ]


# noinspection PyTypeChecker
class RTCA2IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clHeader_clMyRTCAData_ulMessageIdentifier", c_ulong),
                ("clHeader_clMyRTCAData_ulRefStation", c_ulong),
                ("clHeader_clMyRTCAData_ulMessageType", c_ulong),
                ("clHeader_clMyRTCAData_ulReserved", c_ulong),
                ("clHeader_clMyRTCAData_ulMessageLength", c_ulong),
                ("clMyRTCAData_ModifiedZCount", c_double),
                ("clMyRTCAData_AEB", c_char),
                ("clMyRTCAData_Corrections_arraylength", c_ulong),
                ("clMyRTCAData_Corrections", RTCA2IN_clMyRTCAData_Corrections*72),
                ]


# noinspection PyTypeChecker
class RTCADATA2OBS_clMyRTCAObs2_Transmitter2Data(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("L1LockTime", c_char),
                ("L1PsrOffset", c_double),
                ("L1ADROffset", c_double),
                ("FreqAvail", c_char),
                ("CodeType", c_char),
                ("Reserved", c_char),
                ("L2LockTime", c_char),
                ("L2PsrOffset", c_double),
                ("L2ADROffset", c_double),
                ("CodeType2", c_char),
                ("Reserved2", c_char),
                ]


# noinspection PyTypeChecker
class RTCADATA2OBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAObs2_NovAtelDesignator", c_char),
                ("clMyRTCAObs2_SubtypeIndicator", c_char),
                ("clMyRTCAObs2_ReceiverTimeBias", c_double),
                ("clMyRTCAObs2_Seconds", c_float),
                ("clMyRTCAObs2_GloCalibrationQual", c_char),
                ("clMyRTCAObs2_Reserved", c_int),
                ("clMyRTCAObs2_Transmitter2Data_arraylength", c_ulong),
                ("clMyRTCAObs2_Transmitter2Data", RTCADATA2OBS_clMyRTCAObs2_Transmitter2Data*72),
                ]


# noinspection PyTypeChecker
class CORRIMUDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("adMyCorr_wb_ib", c_double*3),
                ("adMyCorr_fb", c_double*3),
                ]


# noinspection PyTypeChecker
class CORRIMUDATAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("adMyCorr_wb_ib", c_double*3),
                ("adMyCorr_fb", c_double*3),
                ]


# noinspection PyTypeChecker
class VISIONREFLIST_aclMyRefList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyRefName", c_char*12),
                ("ulMyReserved", c_ulong),
                ]


# noinspection PyTypeChecker
class VISIONREFLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyRefList_arraylength", c_ulong),
                ("aclMyRefList", VISIONREFLIST_aclMyRefList*16),
                ]


# noinspection PyTypeChecker
class RAWLBANDPREVITERBI(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucData_Len", c_ulong),
                ("aucData", c_char*1024),
                ]


# noinspection PyTypeChecker
class RTCM1014(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3AuxStation_MessageNumber", c_ushort),
                ("clMyRTCMV3AuxStation_NetworkID", c_char),
                ("clMyRTCMV3AuxStation_SubNetworkID", c_char),
                ("clMyRTCMV3AuxStation_NumAuxStationsTransmitted", c_char),
                ("clMyRTCMV3AuxStation_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3AuxStation_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3AuxStation_AuxMasterDeltaLat", c_long),
                ("clMyRTCMV3AuxStation_AuxMasterDeltaLon", c_long),
                ("clMyRTCMV3AuxStation_AuxMasterDeltaHeight", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1014IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3AuxStation_MessageNumber", c_ushort),
                ("clMyRTCMV3AuxStation_NetworkID", c_char),
                ("clMyRTCMV3AuxStation_SubNetworkID", c_char),
                ("clMyRTCMV3AuxStation_NumAuxStationsTransmitted", c_char),
                ("clMyRTCMV3AuxStation_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3AuxStation_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3AuxStation_AuxMasterDeltaLat", c_long),
                ("clMyRTCMV3AuxStation_AuxMasterDeltaLon", c_long),
                ("clMyRTCMV3AuxStation_AuxMasterDeltaHeight", c_long),
                ]


# noinspection PyTypeChecker
class EXTRXHWLEVELS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("HwLevels_fMySystemVoltage", c_float),
                ("HwLevels_fMyMinosVoltage", c_float),
                ("HwLevels_fMyRF2Voltage", c_float),
                ("HwLevels_fMyRF3Voltage", c_float),
                ("HwLevels_fMyCurrentSense", c_float),
                ("HwLevels_fMyExtReserved1", c_float),
                ("HwLevels_fMyExtReserved2", c_float),
                ("HwLevels_fMyExtReserved3", c_float),
                ("HwLevels_fMyExtReserved4", c_float),
                ("HwLevels_fMyExtReserved5", c_float),
                ]


# noinspection PyTypeChecker
class RTCM1007(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_DescriptorCounter", c_char),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1007IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_DescriptorCounter", c_char),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1008(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_DescriptorCounter", c_char),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ("clMyRTCMV3REF_SerialNumberCounter", c_char),
                ("clMyRTCMV3REF_AntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class RTCM1008IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_DescriptorCounter", c_char),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ("clMyRTCMV3REF_SerialNumberCounter", c_char),
                ("clMyRTCMV3REF_AntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class RTCMDATA1007(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1008(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ("clMyRTCMV3REF_AntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class GLMLA_aclMySatAlmData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySlot", c_char),
                ("ucMyHealth", c_char),
                ("cMyFrequency", c_char),
                ("dMyEcc", c_double),
                ("dMyDeltaTD", c_double),
                ("dMyArgPerig", c_double),
                ("dMyDeltaT", c_double),
                ("dMyTLambdaN", c_double),
                ("dMyLambdaN", c_double),
                ("dMyDeltaI", c_double),
                ("dMyTau", c_double),
                ]


# noinspection PyTypeChecker
class GLMLA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNA", c_ulong),
                ("dMyTauC", c_double),
                ("aclMySatAlmData_arraylength", c_ulong),
                ("aclMySatAlmData", GLMLA_aclMySatAlmData*24),
                ]


# noinspection PyTypeChecker
class RTCM31_clMyRTCM31_34Data_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM31(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM31_34Data_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulRefID", c_ulong),
                ("clMyRTCM31_34Data_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM31_34Data_aclMyDiffData", RTCM31_clMyRTCM31_34Data_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCM31IN_clMyRTCM_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM31IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyHealth", c_ulong),
                ("clMyRTCM_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM_aclMyDiffData", RTCM31IN_clMyRTCM_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCM34_clMyRTCM34_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM34(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM34_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM34_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMyHealth", c_ulong),
                ("clMyRTCM34_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM34_aclMyDiffData", RTCM34_clMyRTCM34_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCM34IN_clMyRTCM_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM34IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyHealth", c_ulong),
                ("clMyRTCM_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM_aclMyDiffData", RTCM34IN_clMyRTCM_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCMDATA31_clMyRTCM31_34Data_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA31(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM31_34Data_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyHealth", c_ulong),
                ("clMyRTCM31_34Data_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM31_34Data_aclMyDiffData", RTCMDATA31_clMyRTCM31_34Data_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCMDATA34_clMyRTCM34_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA34(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM34_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM34_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM34_ulMyHealth", c_ulong),
                ("clMyRTCM34_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM34_aclMyDiffData", RTCMDATA34_clMyRTCM34_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCM32(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM32_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM32_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCM32_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCM32_dMyECEF_Z", c_double),
                ]


# noinspection PyTypeChecker
class RTCM32IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCMREF_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCMREF_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCMREF_dMyECEF_Z", c_double),
                ]


# noinspection PyTypeChecker
class RTCM36(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM36_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM36_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM36_aucMyRTCM36Text_Len", c_ulong),
                ("clMyRTCMBody_clMyRTCM36_aucMyRTCM36Text", c_char*90),
                ]


# noinspection PyTypeChecker
class RTCM36IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM36_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM36_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM36_aucMyRTCM36Text_Len", c_ulong),
                ("clMyRTCMBody_clMyRTCM36_aucMyRTCM36Text", c_char*90),
                ]


# noinspection PyTypeChecker
class RTCM36T(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyText", c_char*90),
                ]


# noinspection PyTypeChecker
class RTCMDATA32(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM32_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM32_ulMyHealth", c_ulong),
                ("clMyRTCMREFData_clMyRTCM32_dMyECEF_X", c_double),
                ("clMyRTCMREFData_clMyRTCM32_dMyECEF_Y", c_double),
                ("clMyRTCMREFData_clMyRTCM32_dMyECEF_Z", c_double),
                ]


# noinspection PyTypeChecker
class RTCMDATA36(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM36_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM36_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM36_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM36_aucMyRTCM36Text_Len", c_ulong),
                ("clMyRTCMBody_clMyRTCM36_aucMyRTCM36Text", c_char*90),
                ]


# noinspection PyTypeChecker
class PSRTIME_clMySystemTimeOffsets_aclMySystemOffsets(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("dMyBias", c_double),
                ("dMyBiasStdDev", c_double),
                ]


# noinspection PyTypeChecker
class PSRTIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySystemTimeOffsets_aclMySystemOffsets_arraylength", c_ulong),
                ("clMySystemTimeOffsets_aclMySystemOffsets", PSRTIME_clMySystemTimeOffsets_aclMySystemOffsets*5),
                ]


# noinspection PyTypeChecker
class CMRGLOOBS_clMyType3Message_aclMyCMRBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySlotNumber", c_ulong),
                ("bMyCodeFlag", c_bool),
                ("bMyL1PhaseValid", c_bool),
                ("bMyIsL2Present", c_bool),
                ("ulMyL1Psr", c_ulong),
                ("lMyL1CarrierOffset", c_long),
                ("ulMyL1Snr", c_ulong),
                ("ulMyL1SlipCount", c_ulong),
                ("bMyIsL2Code", c_bool),
                ("bMyCodeType", c_bool),
                ("bMyIsL2CodeValid", c_bool),
                ("bMyIsL2PhaseValid", c_bool),
                ("bMyPhaseFull", c_bool),
                ("ulMyReserved", c_ulong),
                ("lMyL2RangeOffset", c_long),
                ("lMyL2CarrierOffset", c_long),
                ("ulMyL2Snr", c_ulong),
                ("ulMyL2SlipCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CMRGLOOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyType3Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyType3Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyType3Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyType3Message_ulMyLength", c_ulong),
                ("clMyType3Message_ulMyVersion", c_ulong),
                ("clMyType3Message_ulMyStationID", c_ulong),
                ("clMyType3Message_ulMessageType", c_ulong),
                ("clMyType3Message_ulMyNumberofSv", c_ulong),
                ("clMyType3Message_ulMyEpochTime", c_ulong),
                ("clMyType3Message_ulMyClockBiasValid", c_ulong),
                ("clMyType3Message_lMyClockOffset", c_long),
                ("clMyType3Message_aclMyCMRBody_arraylength", c_ulong),
                ("clMyType3Message_aclMyCMRBody", CMRGLOOBS_clMyType3Message_aclMyCMRBody*24),
                ]


# noinspection PyTypeChecker
class CMRGLOOBSIN_clMyCMROBS_aclMyCMRBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySlotNumber", c_ulong),
                ("bMyCodeFlag", c_bool),
                ("bMyL1PhaseValid", c_bool),
                ("bMyIsL2Present", c_bool),
                ("ulMyL1Psr", c_ulong),
                ("lMyL1CarrierOffset", c_long),
                ("ulMyL1Snr", c_ulong),
                ("ulMyL1SlipCount", c_ulong),
                ("bMyIsL2Code", c_bool),
                ("bMyCodeType", c_bool),
                ("bMyIsL2CodeValid", c_bool),
                ("bMyIsL2PhaseValid", c_bool),
                ("bMyPhaseFull", c_bool),
                ("ulMyReserved", c_ulong),
                ("lMyL2RangeOffset", c_long),
                ("lMyL2CarrierOffset", c_long),
                ("ulMyL2Snr", c_ulong),
                ("ulMyL2SlipCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CMRGLOOBSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyCMROBS_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyCMROBS_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyCMROBS_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyCMROBS_ulMyLength", c_ulong),
                ("clMyCMROBS_ulMyVersion", c_ulong),
                ("clMyCMROBS_ulMyStationID", c_ulong),
                ("clMyCMROBS_ulMessageType", c_ulong),
                ("clMyCMROBS_ulMyNumberofSv", c_ulong),
                ("clMyCMROBS_ulMyEpochTime", c_ulong),
                ("clMyCMROBS_ulMyClockBiasValid", c_ulong),
                ("clMyCMROBS_lMyClockOffset", c_long),
                ("clMyCMROBS_aclMyCMRBody_arraylength", c_ulong),
                ("clMyCMROBS_aclMyCMRBody", CMRGLOOBSIN_clMyCMROBS_aclMyCMRBody*24),
                ]


# noinspection PyTypeChecker
class RTCM1009_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1009(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1009_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1009IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1009IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1009IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1010_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1010(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1010_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1010IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1010IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1010IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1011_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1011(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1011_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1011IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1011IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1011IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1012_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ("L2CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1012(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1012_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1012IN_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ("L2CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1012IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCM1012IN_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1019(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGPSEphemerides_MessageNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSatelliteID", c_char),
                ("clMyGPSEphemerides_GPSWeekNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSVAccuracy", c_char),
                ("clMyGPSEphemerides_GPSCodeOnL2", c_char),
                ("clMyGPSEphemerides_GPSIDOT", c_short),
                ("clMyGPSEphemerides_GPSIODE", c_char),
                ("clMyGPSEphemerides_GPSToc", c_ushort),
                ("clMyGPSEphemerides_GPSAf2", c_char),
                ("clMyGPSEphemerides_GPSAf1", c_short),
                ("clMyGPSEphemerides_GPSAf0", c_long),
                ("clMyGPSEphemerides_GPSIODC", c_ushort),
                ("clMyGPSEphemerides_GPSCrs", c_short),
                ("clMyGPSEphemerides_GPSDeltaN", c_short),
                ("clMyGPSEphemerides_GPSM0", c_long),
                ("clMyGPSEphemerides_GPSCuc", c_short),
                ("clMyGPSEphemerides_GPSEcc", c_ulong),
                ("clMyGPSEphemerides_GPSCus", c_short),
                ("clMyGPSEphemerides_GPSSqrRootA", c_ulong),
                ("clMyGPSEphemerides_GPSToe", c_ushort),
                ("clMyGPSEphemerides_GPSCic", c_short),
                ("clMyGPSEphemerides_GPSOmega0", c_long),
                ("clMyGPSEphemerides_GPSCis", c_short),
                ("clMyGPSEphemerides_GPSI0", c_long),
                ("clMyGPSEphemerides_GPSCrc", c_short),
                ("clMyGPSEphemerides_GPSOmega", c_long),
                ("clMyGPSEphemerides_GPSOmegaDot", c_long),
                ("clMyGPSEphemerides_GPSTgd", c_char),
                ("clMyGPSEphemerides_GPSSVHealth", c_char),
                ("clMyGPSEphemerides_GPSL2PDataFlag", c_char),
                ("clMyGPSEphemerides_GPSFitInterval", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1019IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGPSEphemerides_MessageNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSatelliteID", c_char),
                ("clMyGPSEphemerides_GPSWeekNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSVAccuracy", c_char),
                ("clMyGPSEphemerides_GPSCodeOnL2", c_char),
                ("clMyGPSEphemerides_GPSIDOT", c_short),
                ("clMyGPSEphemerides_GPSIODE", c_char),
                ("clMyGPSEphemerides_GPSToc", c_ushort),
                ("clMyGPSEphemerides_GPSAf2", c_char),
                ("clMyGPSEphemerides_GPSAf1", c_short),
                ("clMyGPSEphemerides_GPSAf0", c_long),
                ("clMyGPSEphemerides_GPSIODC", c_ushort),
                ("clMyGPSEphemerides_GPSCrs", c_short),
                ("clMyGPSEphemerides_GPSDeltaN", c_short),
                ("clMyGPSEphemerides_GPSM0", c_long),
                ("clMyGPSEphemerides_GPSCuc", c_short),
                ("clMyGPSEphemerides_GPSEcc", c_ulong),
                ("clMyGPSEphemerides_GPSCus", c_short),
                ("clMyGPSEphemerides_GPSSqrRootA", c_ulong),
                ("clMyGPSEphemerides_GPSToe", c_ushort),
                ("clMyGPSEphemerides_GPSCic", c_short),
                ("clMyGPSEphemerides_GPSOmega0", c_long),
                ("clMyGPSEphemerides_GPSCis", c_short),
                ("clMyGPSEphemerides_GPSI0", c_long),
                ("clMyGPSEphemerides_GPSCrc", c_short),
                ("clMyGPSEphemerides_GPSOmega", c_long),
                ("clMyGPSEphemerides_GPSOmegaDot", c_long),
                ("clMyGPSEphemerides_GPSTgd", c_char),
                ("clMyGPSEphemerides_GPSSVHealth", c_char),
                ("clMyGPSEphemerides_GPSL2PDataFlag", c_char),
                ("clMyGPSEphemerides_GPSFitInterval", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1020(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGLOEphem_MessageNumber", c_ushort),
                ("clMyGLOEphem_GLOSatelliteID", c_char),
                ("clMyGLOEphem_GLOSatelliteFreqChanNumber", c_char),
                ("clMyGLOEphem_GLOAlmanacHealth", c_char),
                ("clMyGLOEphem_GLOAlmanacHealthAvailability", c_char),
                ("clMyGLOEphem_GLOP1", c_char),
                ("clMyGLOEphem_GLOTk", c_ushort),
                ("clMyGLOEphem_GLOMSBBn", c_char),
                ("clMyGLOEphem_GLOP2", c_char),
                ("clMyGLOEphem_GLOTb", c_char),
                ("clMyGLOEphem_GLOXnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOXnTb", c_long),
                ("clMyGLOEphem_GLOXnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOYnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOYnTb", c_long),
                ("clMyGLOEphem_GLOYnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOZnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOZnTb", c_long),
                ("clMyGLOEphem_GLOZnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOP3", c_char),
                ("clMyGLOEphem_GLOGammaTb", c_short),
                ("clMyGLOEphem_GLOMP", c_char),
                ("clMyGLOEphem_GLOMlnThirdString", c_char),
                ("clMyGLOEphem_GLOTauTb", c_long),
                ("clMyGLOEphem_GLOMDeltaTau", c_char),
                ("clMyGLOEphem_GLOEn", c_char),
                ("clMyGLOEphem_GLOMP4", c_char),
                ("clMyGLOEphem_GLOMFt", c_char),
                ("clMyGLOEphem_GLOMNt", c_ushort),
                ("clMyGLOEphem_GLOMM", c_char),
                ("clMyGLOEphem_GLOAvailability", c_char),
                ("clMyGLOEphem_GLONa", c_ushort),
                ("clMyGLOEphem_GLOTauC", c_long),
                ("clMyGLOEphem_GLOMN4", c_char),
                ("clMyGLOEphem_GLOMTauGPS", c_long),
                ("clMyGLOEphem_GLOMlnFifthString", c_char),
                ("clMyGLOEphem_Reserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1020IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGLOEphem_MessageNumber", c_ushort),
                ("clMyGLOEphem_GLOSatelliteID", c_char),
                ("clMyGLOEphem_GLOSatelliteFreqChanNumber", c_char),
                ("clMyGLOEphem_GLOAlmanacHealth", c_char),
                ("clMyGLOEphem_GLOAlmanacHealthAvailability", c_char),
                ("clMyGLOEphem_GLOP1", c_char),
                ("clMyGLOEphem_GLOTk", c_ushort),
                ("clMyGLOEphem_GLOMSBBn", c_char),
                ("clMyGLOEphem_GLOP2", c_char),
                ("clMyGLOEphem_GLOTb", c_char),
                ("clMyGLOEphem_GLOXnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOXnTb", c_long),
                ("clMyGLOEphem_GLOXnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOYnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOYnTb", c_long),
                ("clMyGLOEphem_GLOYnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOZnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOZnTb", c_long),
                ("clMyGLOEphem_GLOZnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOP3", c_char),
                ("clMyGLOEphem_GLOGammaTb", c_short),
                ("clMyGLOEphem_GLOMP", c_char),
                ("clMyGLOEphem_GLOMlnThirdString", c_char),
                ("clMyGLOEphem_GLOTauTb", c_long),
                ("clMyGLOEphem_GLOMDeltaTau", c_char),
                ("clMyGLOEphem_GLOEn", c_char),
                ("clMyGLOEphem_GLOMP4", c_char),
                ("clMyGLOEphem_GLOMFt", c_char),
                ("clMyGLOEphem_GLOMNt", c_ushort),
                ("clMyGLOEphem_GLOMM", c_char),
                ("clMyGLOEphem_GLOAvailability", c_char),
                ("clMyGLOEphem_GLONa", c_ushort),
                ("clMyGLOEphem_GLOTauC", c_long),
                ("clMyGLOEphem_GLOMN4", c_char),
                ("clMyGLOEphem_GLOMTauGPS", c_long),
                ("clMyGLOEphem_GLOMlnFifthString", c_char),
                ("clMyGLOEphem_Reserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1009_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1009(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1009_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1010_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1010(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1010_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1011_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1011(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1011_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1012_clMyRTCMV3OBS_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("L1CodeIndicator", c_char),
                ("FreqChannelNumber", c_char),
                ("L1PSR", c_ulong),
                ("L1PhaseRangeMinusL1PSR", c_long),
                ("L1LockTimeIndicator", c_char),
                ("IntegerL1PSRModulusAmb", c_char),
                ("L1CNR", c_char),
                ("L2CodeIndicator", c_char),
                ("L1L2PSRDiff", c_short),
                ("L2PhaseRangeMinusL1PSR", c_long),
                ("L2LockTimeIndicator", c_char),
                ("L2CNR", c_char),
                ("usReserved", c_ushort),
                ]


# noinspection PyTypeChecker
class RTCMDATA1012(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3OBS_MessageNumber", c_ushort),
                ("clMyRTCMV3OBS_ReferenceStationID", c_ushort),
                ("clMyRTCMV3OBS_EpochTime", c_ulong),
                ("clMyRTCMV3OBS_GNSSMessageFlag", c_char),
                ("clMyRTCMV3OBS_NumSignals", c_char),
                ("clMyRTCMV3OBS_SmoothingIndicator", c_char),
                ("clMyRTCMV3OBS_SmoothingInterval", c_char),
                ("clMyRTCMV3OBS_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3OBS_aclBodyData", RTCMDATA1012_clMyRTCMV3OBS_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCMDATA1019(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGPSEphemerides_MessageNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSatelliteID", c_char),
                ("clMyGPSEphemerides_GPSWeekNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSVAccuracy", c_char),
                ("clMyGPSEphemerides_GPSCodeOnL2", c_char),
                ("clMyGPSEphemerides_GPSIDOT", c_short),
                ("clMyGPSEphemerides_GPSIODE", c_char),
                ("clMyGPSEphemerides_GPSToc", c_ushort),
                ("clMyGPSEphemerides_GPSAf2", c_char),
                ("clMyGPSEphemerides_GPSAf1", c_short),
                ("clMyGPSEphemerides_GPSAf0", c_long),
                ("clMyGPSEphemerides_GPSIODC", c_ushort),
                ("clMyGPSEphemerides_GPSCrs", c_short),
                ("clMyGPSEphemerides_GPSDeltaN", c_short),
                ("clMyGPSEphemerides_GPSM0", c_long),
                ("clMyGPSEphemerides_GPSCuc", c_short),
                ("clMyGPSEphemerides_GPSEcc", c_ulong),
                ("clMyGPSEphemerides_GPSCus", c_short),
                ("clMyGPSEphemerides_GPSSqrRootA", c_ulong),
                ("clMyGPSEphemerides_GPSToe", c_ushort),
                ("clMyGPSEphemerides_GPSCic", c_short),
                ("clMyGPSEphemerides_GPSOmega0", c_long),
                ("clMyGPSEphemerides_GPSCis", c_short),
                ("clMyGPSEphemerides_GPSI0", c_long),
                ("clMyGPSEphemerides_GPSCrc", c_short),
                ("clMyGPSEphemerides_GPSOmega", c_long),
                ("clMyGPSEphemerides_GPSOmegaDot", c_long),
                ("clMyGPSEphemerides_GPSTgd", c_char),
                ("clMyGPSEphemerides_GPSSVHealth", c_char),
                ("clMyGPSEphemerides_GPSL2PDataFlag", c_char),
                ("clMyGPSEphemerides_GPSFitInterval", c_char),
                ]


# noinspection PyTypeChecker
class RTCMDATA1020(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGLOEphem_MessageNumber", c_ushort),
                ("clMyGLOEphem_GLOSatelliteID", c_char),
                ("clMyGLOEphem_GLOSatelliteFreqChanNumber", c_char),
                ("clMyGLOEphem_GLOAlmanacHealth", c_char),
                ("clMyGLOEphem_GLOAlmanacHealthAvailability", c_char),
                ("clMyGLOEphem_GLOP1", c_char),
                ("clMyGLOEphem_GLOTk", c_ushort),
                ("clMyGLOEphem_GLOMSBBn", c_char),
                ("clMyGLOEphem_GLOP2", c_char),
                ("clMyGLOEphem_GLOTb", c_char),
                ("clMyGLOEphem_GLOXnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOXnTb", c_long),
                ("clMyGLOEphem_GLOXnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOYnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOYnTb", c_long),
                ("clMyGLOEphem_GLOYnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOZnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOZnTb", c_long),
                ("clMyGLOEphem_GLOZnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOP3", c_char),
                ("clMyGLOEphem_GLOGammaTb", c_short),
                ("clMyGLOEphem_GLOMP", c_char),
                ("clMyGLOEphem_GLOMlnThirdString", c_char),
                ("clMyGLOEphem_GLOTauTb", c_long),
                ("clMyGLOEphem_GLOMDeltaTau", c_char),
                ("clMyGLOEphem_GLOEn", c_char),
                ("clMyGLOEphem_GLOMP4", c_char),
                ("clMyGLOEphem_GLOMFt", c_char),
                ("clMyGLOEphem_GLOMNt", c_ushort),
                ("clMyGLOEphem_GLOMM", c_char),
                ("clMyGLOEphem_GLOAvailability", c_char),
                ("clMyGLOEphem_GLONa", c_ushort),
                ("clMyGLOEphem_GLOTauC", c_long),
                ("clMyGLOEphem_GLOMN4", c_char),
                ("clMyGLOEphem_GLOMTauGPS", c_long),
                ("clMyGLOEphem_GLOMlnFifthString", c_char),
                ("clMyGLOEphem_Reserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCM59GLO_clMyRTCM31_34Data_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM59GLO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM31_34Data_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulRefID", c_ulong),
                ("ucMySubType", c_char),
                ("clMyRTCM31_34Data_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM31_34Data_aclMyDiffData", RTCM59GLO_clMyRTCM31_34Data_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCM59GLOIN_clMyRTCM_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM59GLOIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM_ulMyHealth", c_ulong),
                ("ucMySubtype", c_char),
                ("clMyRTCM_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM_aclMyDiffData", RTCM59GLOIN_clMyRTCM_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class RTCMDATA59GLO_clMyRTCM31_34Data_aclMyDiffData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyScale", c_ulong),
                ("ulMyUDRE", c_ulong),
                ("ulMySvPrn", c_ulong),
                ("iMyCor", c_int),
                ("iMyCorRate", c_int),
                ("ulMyChangeBit", c_ulong),
                ("ulMyTk", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA59GLO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCM31_34Data_ulMyType", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulRefID", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyZcount", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMySequenceNum", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyFrameLength", c_ulong),
                ("clMyHeader_clMyRTCM31_34Data_ulMyHealth", c_ulong),
                ("ucMySubType", c_char),
                ("clMyRTCM31_34Data_aclMyDiffData_arraylength", c_ulong),
                ("clMyRTCM31_34Data_aclMyDiffData", RTCMDATA59GLO_clMyRTCM31_34Data_aclMyDiffData*24),
                ]


# noinspection PyTypeChecker
class EXTREFSTATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStatus", c_ulong),
                ("ulMyGpsWeek", c_ulong),
                ("ulMyGPSSeconds", c_ulong),
                ("dMyX", c_double),
                ("dMyY", c_double),
                ("dMyZ", c_double),
                ("ulMyHealth", c_ulong),
                ("eMyRefType", c_uint),
                ("acMyStationID", c_char*5),
                ("fMyARPHeight", c_float),
                ("eMySolutionStatus", c_uint),
                ("eMyPositionType", c_uint),
                ("fMyDifferentialAge", c_float),
                ("ulMyReserved1", c_ulong),
                ("ulMyReserved2", c_ulong),
                ]


# noinspection PyTypeChecker
class RTKDOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyHTDOP", c_float),
                ("clMyDOPs_fMyTDOP", c_float),
                ("clMyDOPs_fMyGPSElevMask", c_float),
                ("clMyDOPs_aulMySats_Len", c_ulong),
                ("clMyDOPs_aulMySats", c_ulong*325),
                ]


# noinspection PyTypeChecker
class HWMONITOR_aclMyMeasurements(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyValue", c_float),
                ("ulMyStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class HWMONITOR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyMeasurements_arraylength", c_ulong),
                ("aclMyMeasurements", HWMONITOR_aclMyMeasurements*32),
                ]


# noinspection PyTypeChecker
class RTCMDATA22GG_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulSpareBits", c_ulong),
                ("ulMyConstellation", c_ulong),
                ("ulMyAntennaType", c_ulong),
                ("ulMyAntennaRefPoint", c_ulong),
                ("bNoHeight", c_bool),
                ("ulAntennaPhaseHeight", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCMDATA22GG_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyL2AntDeltaX", c_long),
                ("lMyL2AntDeltaY", c_long),
                ("lMyL2AntDeltaZ", c_long),
                ]


# noinspection PyTypeChecker
class RTCMDATA22GG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMHeader_clMyRTCM22_ulMyType", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulRefID", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyZcount", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMySequenceNum", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyFrameLength", c_ulong),
                ("clMyRTCMHeader_clMyRTCM22_ulMyHealth", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaX", c_long),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaY", c_long),
                ("clMyRTCMBody_clMyRTCM22_lMyL1AntDeltaZ", c_long),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1_arraylength", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1", RTCMDATA22GG_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntHgtL1*1),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2_arraylength", c_ulong),
                ("clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2", RTCMDATA22GG_clMyRTCMBody_clMyRTCM22_clMyRTCM22AntInfL2*1),
                ]


# noinspection PyTypeChecker
class HEADING(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("fFloat", c_float),
                ("clMyHeadingInfo_fMyHeadingStdDev", c_float),
                ("clMyHeadingInfo_fMyPitchStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class RAWSBASFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iMyFrameDecoderNum", c_int),
                ("ulMyPrn", c_ulong),
                ("ulMyWAASMsgId", c_ulong),
                ("aucMyRawFrameData", c_char*29),
                ("ulMySignalChannelNum", c_ulong),
                ]


# noinspection PyTypeChecker
class RAWGLOFRAME_aclMyRawString(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyString", c_char*11),
                ("ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class RAWGLOFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyFrameNumber", c_ulong),
                ("usMySloto", c_ushort),
                ("usMyFreqo", c_ushort),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("ulMyFrameDecoderNumber", c_ulong),
                ("ulMySignalChannelNumber", c_ulong),
                ("aclMyRawString_arraylength", c_ulong),
                ("aclMyRawString", RAWGLOFRAME_aclMyRawString*15),
                ]


# noinspection PyTypeChecker
class RAWGLOSTRING(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySlot", c_char),
                ("cMyFreq", c_char),
                ("clMyStringBuffer_aucMyString", c_char*11),
                ("clMyStringBuffer_ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class SBAS0(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("aucMyPRNMask", c_char*27),
                ("ulMyIODP", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS10(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyBrrc", c_ulong),
                ("ulMyCltc_lsb", c_ulong),
                ("ulMyCltc_v1", c_ulong),
                ("ulMyIltc_v1", c_ulong),
                ("ulMyCltc_v0", c_ulong),
                ("ulMyIltc_v0", c_ulong),
                ("ulMyCgeo_lsb", c_ulong),
                ("ulMyCgeo_v", c_ulong),
                ("ulMyIgeo", c_ulong),
                ("ulMyCer", c_ulong),
                ("ulMyCiono_step", c_ulong),
                ("ulMyIiono", c_ulong),
                ("ulMyCiono_ramp", c_ulong),
                ("ulMyRSSUDRE", c_ulong),
                ("ulMyRSSIono", c_ulong),
                ("aulMySpareBits", c_char*11),
                ]


# noinspection PyTypeChecker
class SBAS12(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("dMyA1", c_double),
                ("dMyA0", c_double),
                ("ulMyt0t", c_ulong),
                ("usMyWN", c_ushort),
                ("sMyDtLS", c_short),
                ("usMyWNLSF", c_ushort),
                ("usMyDN", c_ushort),
                ("usMyDtLSF", c_short),
                ("usMyUTCID", c_ushort),
                ("ulMyGPSTOW", c_ulong),
                ("ulMyGPSWN", c_ulong),
                ("bMyGlonassIndicator", c_bool),
                ("aucMyReservedBits", c_char*10),
                ]


# noinspection PyTypeChecker
class SBAS17_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyDataID", c_ushort),
                ("usMyPRN", c_ushort),
                ("usMyHealth", c_ushort),
                ("lMyX", c_long),
                ("lMyY", c_long),
                ("lMyZ", c_long),
                ("lMyXVel", c_long),
                ("lMyYVel", c_long),
                ("lMyZVel", c_long),
                ]


# noinspection PyTypeChecker
class SBAS17(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", SBAS17_aclMyEntries*3),
                ("ulMyt0", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS18(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyNumBands", c_ulong),
                ("ulMyBandNum", c_ulong),
                ("ulMyIODI", c_ulong),
                ("aucMyIGPMask", c_char*26),
                ("ulMySpareBit", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class SBAS24(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("alMyPRC", c_long*6),
                ("aulMyUDREI", c_ulong*6),
                ("ulMyIODP", c_ulong),
                ("ulMyBlockID", c_ulong),
                ("ulMyIODF", c_ulong),
                ("ulMySpare", c_ulong),
                ("clMySlowCorrections_ulMyVelocityCode", c_ulong),
                ("clMySlowCorrections_ulMyPRNMaskNumber1", c_ulong),
                ("clMySlowCorrections_ulMyIODE1", c_ulong),
                ("clMySlowCorrections_lMyDX1", c_long),
                ("clMySlowCorrections_lMyDY1", c_long),
                ("clMySlowCorrections_lMyDZ1", c_long),
                ("clMySlowCorrections_lMyaF01", c_long),
                ("clMySlowCorrections_ulMyPRNMaskNumber2", c_ulong),
                ("clMySlowCorrections_ulMyIODE2", c_ulong),
                ("clMySlowCorrections_lMyDX2orDDX", c_long),
                ("clMySlowCorrections_lMyDY2orDDY", c_long),
                ("clMySlowCorrections_lMyDZ2orDDZ", c_long),
                ("clMySlowCorrections_lMyaF02oraF1", c_long),
                ("clMySlowCorrections_ulMyTOD", c_ulong),
                ("clMySlowCorrections_ulMyIODP", c_ulong),
                ("clMySlowCorrections_ulMySpare", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS25(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFirstHalf_ulMyVelocityCode", c_ulong),
                ("clMyFirstHalf_ulMyPRNMaskNumber1", c_ulong),
                ("clMyFirstHalf_ulMyIODE1", c_ulong),
                ("clMyFirstHalf_lMyDX1", c_long),
                ("clMyFirstHalf_lMyDY1", c_long),
                ("clMyFirstHalf_lMyDZ1", c_long),
                ("clMyFirstHalf_lMyaF01", c_long),
                ("clMyFirstHalf_ulMyPRNMaskNumber2", c_ulong),
                ("clMyFirstHalf_ulMyIODE2", c_ulong),
                ("clMyFirstHalf_lMyDX2orDDX", c_long),
                ("clMyFirstHalf_lMyDY2orDDY", c_long),
                ("clMyFirstHalf_lMyDZ2orDDZ", c_long),
                ("clMyFirstHalf_lMyaF02oraF1", c_long),
                ("clMyFirstHalf_ulMyTOD", c_ulong),
                ("clMyFirstHalf_ulMyIODP", c_ulong),
                ("clMyFirstHalf_ulMySpare", c_ulong),
                ("clMySecondHalf_ulMyVelocityCode", c_ulong),
                ("clMySecondHalf_ulMyPRNMaskNumber1", c_ulong),
                ("clMySecondHalf_ulMyIODE1", c_ulong),
                ("clMySecondHalf_lMyDX1", c_long),
                ("clMySecondHalf_lMyDY1", c_long),
                ("clMySecondHalf_lMyDZ1", c_long),
                ("clMySecondHalf_lMyaF01", c_long),
                ("clMySecondHalf_ulMyPRNMaskNumber2", c_ulong),
                ("clMySecondHalf_ulMyIODE2", c_ulong),
                ("clMySecondHalf_lMyDX2orDDX", c_long),
                ("clMySecondHalf_lMyDY2orDDY", c_long),
                ("clMySecondHalf_lMyDZ2orDDZ", c_long),
                ("clMySecondHalf_lMyaF02oraF1", c_long),
                ("clMySecondHalf_ulMyTOD", c_ulong),
                ("clMySecondHalf_ulMyIODP", c_ulong),
                ("clMySecondHalf_ulMySpare", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS26_aclMyGridPointData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyIGPVDE", c_ulong),
                ("ulMyGIVEI", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS26(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyBandNum", c_ulong),
                ("ulMyBlockID", c_ulong),
                ("aclMyGridPointData_arraylength", c_ulong),
                ("aclMyGridPointData", SBAS26_aclMyGridPointData*15),
                ("ulMyIODI", c_ulong),
                ("ulMySpareBits", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS27_aclMyRegions(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyLat1", c_long),
                ("lMyLong1", c_long),
                ("lMyLat2", c_long),
                ("lMyLong2", c_long),
                ("ulMyShape", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS27(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODS", c_ulong),
                ("ulMyNumServiceMsgs", c_ulong),
                ("ulMyServiceMsgNum", c_ulong),
                ("ulMyPriorityCode", c_ulong),
                ("ulMyUDREInside", c_ulong),
                ("ulMyUDREOutside", c_ulong),
                ("aclMyRegions_arraylength", c_ulong),
                ("aclMyRegions", SBAS27_aclMyRegions*5),
                ("ulMyReserved", c_ulong),
                ("ulMyt0", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class SBAS32(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class SBAS33(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class SBAS34(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class SBAS35(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*11),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*11),
                ]


# noinspection PyTypeChecker
class SBAS4(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class SBAS45(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFirstHalf_ulMyPRNMaskNumber", c_ulong),
                ("clMyFirstHalf_ulMyIODE", c_ulong),
                ("clMyFirstHalf_lMyDX", c_long),
                ("clMyFirstHalf_lMyDY", c_long),
                ("clMyFirstHalf_lMyDZ", c_long),
                ("clMyFirstHalf_lMyDDX", c_long),
                ("clMyFirstHalf_lMyDDY", c_long),
                ("clMyFirstHalf_lMyDDZ", c_long),
                ("clMyFirstHalf_lMyDAF0", c_long),
                ("clMyFirstHalf_ulMyTOD", c_ulong),
                ("clMySecondHalf_ulMyPRNMaskNumber", c_ulong),
                ("clMySecondHalf_ulMyIODE", c_ulong),
                ("clMySecondHalf_lMyDX", c_long),
                ("clMySecondHalf_lMyDY", c_long),
                ("clMySecondHalf_lMyDZ", c_long),
                ("clMySecondHalf_lMyDDX", c_long),
                ("clMySecondHalf_lMyDDY", c_long),
                ("clMySecondHalf_lMyDDZ", c_long),
                ("clMySecondHalf_lMyDAF0", c_long),
                ("clMySecondHalf_ulMyTOD", c_ulong),
                ("ulMyIODP", c_ulong),
                ]


# noinspection PyTypeChecker
class SBAS5(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("clMyFastCorrections_IODF", c_ulong),
                ("clMyFastCorrections_IODP", c_ulong),
                ("clMyFastCorrections_alMyPRC", c_long*13),
                ("clMyFastCorrections_aulMyUDREI", c_ulong*13),
                ]


# noinspection PyTypeChecker
class SBAS6(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODF2", c_ulong),
                ("ulMyIODF3", c_ulong),
                ("ulMyIODF4", c_ulong),
                ("ulMyIODF5", c_ulong),
                ("aulMyUDREI", c_ulong*51),
                ]


# noinspection PyTypeChecker
class SBAS7(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMySystemLatency", c_ulong),
                ("ulMyIODP", c_ulong),
                ("ulMySpareBits", c_ulong),
                ("aulMyDegradationFactor", c_ulong*51),
                ]


# noinspection PyTypeChecker
class SBAS9(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODN", c_ulong),
                ("ulMyt0", c_ulong),
                ("ulMyURA", c_ulong),
                ("dMyX", c_double),
                ("dMyY", c_double),
                ("dMyZ", c_double),
                ("dMyXVel", c_double),
                ("dMyYVel", c_double),
                ("dMyZVel", c_double),
                ("dMyXAccel", c_double),
                ("dMyYAccel", c_double),
                ("dMyZAccel", c_double),
                ("dMyaf0", c_double),
                ("dMyaf1", c_double),
                ]


# noinspection PyTypeChecker
class SBASCORR_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("ulMyIODE", c_ulong),
                ("fMyCorrection", c_float),
                ("fMyStdDev", c_float),
                ]


# noinspection PyTypeChecker
class SBASCORR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", SBASCORR_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class CMRDATAGLOOBS_clMyType3Message_aclMyCMRBody(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySlotNumber", c_ulong),
                ("bMyCodeFlag", c_bool),
                ("bMyL1PhaseValid", c_bool),
                ("bMyIsL2Present", c_bool),
                ("ulMyL1Psr", c_ulong),
                ("lMyL1CarrierOffset", c_long),
                ("ulMyL1Snr", c_ulong),
                ("ulMyL1SlipCount", c_ulong),
                ("bMyIsL2Code", c_bool),
                ("bMyCodeType", c_bool),
                ("bMyIsL2CodeValid", c_bool),
                ("bMyIsL2PhaseValid", c_bool),
                ("bMyPhaseFull", c_bool),
                ("ulMyReserved", c_ulong),
                ("lMyL2RangeOffset", c_long),
                ("lMyL2CarrierOffset", c_long),
                ("ulMyL2Snr", c_ulong),
                ("ulMyL2SlipCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CMRDATAGLOOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCMRHeader_clMyType3Message_ulMyCMRSync", c_ulong),
                ("clMyCMRHeader_clMyType3Message_ulMyStatus", c_ulong),
                ("clMyCMRHeader_clMyType3Message_ulMyType", c_ulong),
                ("clMyCMRHeader_clMyType3Message_ulMyLength", c_ulong),
                ("clMyType3Message_ulMyVersion", c_ulong),
                ("clMyType3Message_ulMyStationID", c_ulong),
                ("clMyType3Message_ulMessageType", c_ulong),
                ("clMyType3Message_ulMyNumberofSv", c_ulong),
                ("clMyType3Message_ulMyEpochTime", c_ulong),
                ("clMyType3Message_ulMyClockBiasValid", c_ulong),
                ("clMyType3Message_lMyClockOffset", c_long),
                ("clMyType3Message_aclMyCMRBody_arraylength", c_ulong),
                ("clMyType3Message_aclMyCMRBody", CMRDATAGLOOBS_clMyType3Message_aclMyCMRBody*24),
                ]


# noinspection PyTypeChecker
class RTCM1037_clMyRTCMV3GLONRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ("SatelliteID", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1037(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GLONRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3GLONRTK_NetworkID", c_char),
                ("clMyRTCMV3GLONRTK_SubNetworkID", c_char),
                ("clMyRTCMV3GLONRTK_EpochTime", c_ulong),
                ("clMyRTCMV3GLONRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3GLONRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONRTK_NumSats", c_char),
                ("clMyRTCMV3GLONRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GLONRTK_aclBodyData", RTCM1037_clMyRTCMV3GLONRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1037IN_clMyRTCMV3NRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1037IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3NRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3NRTK_NetworkID", c_char),
                ("clMyRTCMV3NRTK_SubNetworkID", c_char),
                ("clMyRTCMV3NRTK_EpochTime", c_ulong),
                ("clMyRTCMV3NRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3NRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_NumSats", c_char),
                ("clMyRTCMV3NRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3NRTK_aclBodyData", RTCM1037IN_clMyRTCMV3NRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1038_clMyRTCMV3GLONRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1038(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GLONRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3GLONRTK_NetworkID", c_char),
                ("clMyRTCMV3GLONRTK_SubNetworkID", c_char),
                ("clMyRTCMV3GLONRTK_EpochTime", c_ulong),
                ("clMyRTCMV3GLONRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3GLONRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONRTK_NumSats", c_char),
                ("clMyRTCMV3GLONRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GLONRTK_aclBodyData", RTCM1038_clMyRTCMV3GLONRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1038IN_clMyRTCMV3NRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1038IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3NRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3NRTK_NetworkID", c_char),
                ("clMyRTCMV3NRTK_SubNetworkID", c_char),
                ("clMyRTCMV3NRTK_EpochTime", c_ulong),
                ("clMyRTCMV3NRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3NRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_NumSats", c_char),
                ("clMyRTCMV3NRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3NRTK_aclBodyData", RTCM1038IN_clMyRTCMV3NRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1039_clMyRTCMV3GLONRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1039(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GLONRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3GLONRTK_NetworkID", c_char),
                ("clMyRTCMV3GLONRTK_SubNetworkID", c_char),
                ("clMyRTCMV3GLONRTK_EpochTime", c_ulong),
                ("clMyRTCMV3GLONRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3GLONRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONRTK_NumSats", c_char),
                ("clMyRTCMV3GLONRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GLONRTK_aclBodyData", RTCM1039_clMyRTCMV3GLONRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1039IN_clMyRTCMV3NRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1039IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3NRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3NRTK_NetworkID", c_char),
                ("clMyRTCMV3NRTK_SubNetworkID", c_char),
                ("clMyRTCMV3NRTK_EpochTime", c_ulong),
                ("clMyRTCMV3NRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3NRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_NumSats", c_char),
                ("clMyRTCMV3NRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3NRTK_aclBodyData", RTCM1039IN_clMyRTCMV3NRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1015_clMyRTCMV3GPSNRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1015(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GPSNRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3GPSNRTK_NetworkID", c_char),
                ("clMyRTCMV3GPSNRTK_SubNetworkID", c_char),
                ("clMyRTCMV3GPSNRTK_EpochTime", c_ulong),
                ("clMyRTCMV3GPSNRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3GPSNRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3GPSNRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3GPSNRTK_NumSats", c_char),
                ("clMyRTCMV3GPSNRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GPSNRTK_aclBodyData", RTCM1015_clMyRTCMV3GPSNRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1015IN_clMyRTCMV3NRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1015IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3NRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3NRTK_NetworkID", c_char),
                ("clMyRTCMV3NRTK_SubNetworkID", c_char),
                ("clMyRTCMV3NRTK_EpochTime", c_ulong),
                ("clMyRTCMV3NRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3NRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_NumSats", c_char),
                ("clMyRTCMV3NRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3NRTK_aclBodyData", RTCM1015IN_clMyRTCMV3NRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1016_clMyRTCMV3GPSNRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1016(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GPSNRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3GPSNRTK_NetworkID", c_char),
                ("clMyRTCMV3GPSNRTK_SubNetworkID", c_char),
                ("clMyRTCMV3GPSNRTK_EpochTime", c_ulong),
                ("clMyRTCMV3GPSNRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3GPSNRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3GPSNRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3GPSNRTK_NumSats", c_char),
                ("clMyRTCMV3GPSNRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GPSNRTK_aclBodyData", RTCM1016_clMyRTCMV3GPSNRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1016IN_clMyRTCMV3NRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1016IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3NRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3NRTK_NetworkID", c_char),
                ("clMyRTCMV3NRTK_SubNetworkID", c_char),
                ("clMyRTCMV3NRTK_EpochTime", c_ulong),
                ("clMyRTCMV3NRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3NRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_NumSats", c_char),
                ("clMyRTCMV3NRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3NRTK_aclBodyData", RTCM1016IN_clMyRTCMV3NRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1017_clMyRTCMV3GPSNRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1017(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GPSNRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3GPSNRTK_NetworkID", c_char),
                ("clMyRTCMV3GPSNRTK_SubNetworkID", c_char),
                ("clMyRTCMV3GPSNRTK_EpochTime", c_ulong),
                ("clMyRTCMV3GPSNRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3GPSNRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3GPSNRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3GPSNRTK_NumSats", c_char),
                ("clMyRTCMV3GPSNRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GPSNRTK_aclBodyData", RTCM1017_clMyRTCMV3GPSNRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1017IN_clMyRTCMV3NRTK_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("AmbiguityStatusFlag", c_char),
                ("NonSyncCount", c_char),
                ("GeoCarrierPhaseCorrDiff", c_long),
                ("IODE", c_char),
                ("IonoCarrierPhaseCorrDiff", c_long),
                ]


# noinspection PyTypeChecker
class RTCM1017IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3NRTK_MessageNumber", c_ushort),
                ("clMyRTCMV3NRTK_NetworkID", c_char),
                ("clMyRTCMV3NRTK_SubNetworkID", c_char),
                ("clMyRTCMV3NRTK_EpochTime", c_ulong),
                ("clMyRTCMV3NRTK_MultipleMessageIndicator", c_char),
                ("clMyRTCMV3NRTK_MasterReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_AuxReferenceStationID", c_ushort),
                ("clMyRTCMV3NRTK_NumSats", c_char),
                ("clMyRTCMV3NRTK_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3NRTK_aclBodyData", RTCM1017IN_clMyRTCMV3NRTK_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1036_clMyRTCMV3GLONavID_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("GLOSatelliteID", c_char),
                ("GLOSubIOD", c_char),
                ("GLOCRC24", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM1036(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GLONavID_MessageNumber", c_ushort),
                ("clMyRTCMV3GLONavID_ReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONavID_NumGLOData", c_char),
                ("clMyRTCMV3GLONavID_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GLONavID_aclBodyData", RTCM1036_clMyRTCMV3GLONavID_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1036IN_clMyRTCMV3GLONavID_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("GLOSatelliteID", c_char),
                ("GLOSubIOD", c_char),
                ("GLOCRC24", c_ulong),
                ]


# noinspection PyTypeChecker
class RTCM1036IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GLONavID_MessageNumber", c_ushort),
                ("clMyRTCMV3GLONavID_ReferenceStationID", c_ushort),
                ("clMyRTCMV3GLONavID_NumGLOData", c_char),
                ("clMyRTCMV3GLONavID_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GLONavID_aclBodyData", RTCM1036IN_clMyRTCMV3GLONavID_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1034_clMyRTCMV3FKP_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("IODE", c_char),
                ("NorthGeoGradient", c_short),
                ("EastGeoGradient", c_short),
                ("NorthIonoGradient", c_short),
                ("EastIonoGradient", c_short),
                ]


# noinspection PyTypeChecker
class RTCM1034(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3FKP_MessageNumber", c_ushort),
                ("clMyRTCMV3FKP_ReferenceStationID", c_ushort),
                ("clMyRTCMV3FKP_FKPEpochTime", c_ulong),
                ("clMyRTCMV3FKP_NumSats", c_char),
                ("clMyRTCMV3FKP_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3FKP_aclBodyData", RTCM1034_clMyRTCMV3FKP_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1034IN_clMyRTCMV3FKP_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("IODE", c_char),
                ("NorthGeoGradient", c_short),
                ("EastGeoGradient", c_short),
                ("NorthIonoGradient", c_short),
                ("EastIonoGradient", c_short),
                ]


# noinspection PyTypeChecker
class RTCM1034IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3FKP_MessageNumber", c_ushort),
                ("clMyRTCMV3FKP_ReferenceStationID", c_ushort),
                ("clMyRTCMV3FKP_FKPEpochTime", c_ulong),
                ("clMyRTCMV3FKP_NumSats", c_char),
                ("clMyRTCMV3FKP_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3FKP_aclBodyData", RTCM1034IN_clMyRTCMV3FKP_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1035_clMyRTCMV3GLOFKP_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("IODE", c_char),
                ("NorthGeoGradient", c_short),
                ("EastGeoGradient", c_short),
                ("NorthIonoGradient", c_short),
                ("EastIonoGradient", c_short),
                ]


# noinspection PyTypeChecker
class RTCM1035(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3GLOFKP_MessageNumber", c_ushort),
                ("clMyRTCMV3GLOFKP_ReferenceStationID", c_ushort),
                ("clMyRTCMV3GLOFKP_FKPEpochTime", c_ulong),
                ("clMyRTCMV3GLOFKP_NumSats", c_char),
                ("clMyRTCMV3GLOFKP_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3GLOFKP_aclBodyData", RTCM1035_clMyRTCMV3GLOFKP_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class RTCM1035IN_clMyRTCMV3FKP_aclBodyData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SatelliteID", c_char),
                ("IODE", c_char),
                ("NorthGeoGradient", c_short),
                ("EastGeoGradient", c_short),
                ("NorthIonoGradient", c_short),
                ("EastIonoGradient", c_short),
                ]


# noinspection PyTypeChecker
class RTCM1035IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3FKP_MessageNumber", c_ushort),
                ("clMyRTCMV3FKP_ReferenceStationID", c_ushort),
                ("clMyRTCMV3FKP_FKPEpochTime", c_ulong),
                ("clMyRTCMV3FKP_NumSats", c_char),
                ("clMyRTCMV3FKP_aclBodyData_arraylength", c_ulong),
                ("clMyRTCMV3FKP_aclBodyData", RTCM1035IN_clMyRTCMV3FKP_aclBodyData*325),
                ]


# noinspection PyTypeChecker
class SATVIS2_aclMySatVisList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatID_idMyID", satelliteid),
                ("ulMySatHealth", c_ulong),
                ("dMyElevation", c_double),
                ("dMyAzimuth", c_double),
                ("dMyTrueDoppler", c_double),
                ("dMyApparentDoppler", c_double),
                ]


# noinspection PyTypeChecker
class SATVIS2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("bMyIsSatVisValid", c_bool),
                ("bMyWasGNSSAlmanacUsed", c_bool),
                ("aclMySatVisList_arraylength", c_ulong),
                ("aclMySatVisList", SATVIS2_aclMySatVisList*39),
                ]


# noinspection PyTypeChecker
class GPHDT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_bMyOutputHDT", c_bool),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ]


# noinspection PyTypeChecker
class HWCONFIGTABLE_clMyHWConfigTableEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyType", c_char*16),
                ("acMyData", c_char*16),
                ]


# noinspection PyTypeChecker
class HWCONFIGTABLE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNumClearedPackets", c_ulong),
                ("ulMyNumUnusedPackets", c_ulong),
                ("clMyHWConfigTableEntries_arraylength", c_ulong),
                ("clMyHWConfigTableEntries", HWCONFIGTABLE_clMyHWConfigTableEntries*125),
                ]


# noinspection PyTypeChecker
class DEBUGFIQ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyFIQAverageCriticalRunTimeUS", c_float),
                ("fMyFIQMaxCriticalRunTimeUS", c_float),
                ("fMyFIQCriticalRunTimeUS", c_float),
                ("fMyFIQMaxPeriodUS", c_float),
                ("fMyFIQPeriodUS", c_float),
                ("ulMySignalQueueHighWaterMark", c_ulong),
                ("ulMyMiscQueueHighWaterMark", c_ulong),
                ("ulMyFIQRLTMS", c_ulong),
                ]


# noinspection PyTypeChecker
class GLORAWL2FRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySlot", c_char),
                ("cMyFreq", c_char),
                ("ulMySigChan", c_ulong),
                ("aucMyRawFrameData", c_char*63),
                ]


# noinspection PyTypeChecker
class RTCAREFEXT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCAREFEXTData_ucMyNovAtelDesignator", c_char),
                ("clMyRTCAREFEXTData_ucMySubTypeIndicator", c_char),
                ("clMyRTCAREFEXTData_ulMyWeek", c_ulong),
                ("clMyRTCAREFEXTData_dMyRTCATime", c_double),
                ("clMyRTCAREFEXTData_ucMySolStatus", c_char),
                ("clMyRTCAREFEXTData_ucMyPosType", c_char),
                ("clMyRTCAREFEXTData_dMyX", c_double),
                ("clMyRTCAREFEXTData_dMyY", c_double),
                ("clMyRTCAREFEXTData_dMyZ", c_double),
                ("clMyRTCAREFEXTData_dMyStdX", c_double),
                ("clMyRTCAREFEXTData_dMyStdY", c_double),
                ("clMyRTCAREFEXTData_dMyStdZ", c_double),
                ("clMyRTCAREFEXTData_dMyStdXY", c_double),
                ("clMyRTCAREFEXTData_dMyStdYZ", c_double),
                ("clMyRTCAREFEXTData_dMyStdZX", c_double),
                ("clMyRTCAREFEXTData_fMyUndulation", c_float),
                ("clMyRTCAREFEXTData_ucMyNumSatsTracked", c_char),
                ("clMyRTCAREFEXTData_ucMyNumSatsInSol", c_char),
                ("clMyRTCAREFEXTData_ucMyNumHighSats", c_char),
                ("clMyRTCAREFEXTData_ucMyNumHighL2Sats", c_char),
                ("clMyRTCAREFEXTData_ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCAREFEXTIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_clMyRTCAREF_ulMessageIdentifier", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulRefStation", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulMessageType", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulReserved", c_ulong),
                ("clMyHeader_clMyRTCAREF_ulMessageLength", c_ulong),
                ("clMyRTCAREF_ucMyNovAtelDesignator", c_char),
                ("clMyRTCAREF_ucMySubTypeIndicator", c_char),
                ("clMyRTCAREF_ulMyWeek", c_ulong),
                ("clMyRTCAREF_dMyRTCATime", c_double),
                ("clMyRTCAREF_ucMySolStatus", c_char),
                ("clMyRTCAREF_ucMyPosType", c_char),
                ("clMyRTCAREF_dMyX", c_double),
                ("clMyRTCAREF_dMyY", c_double),
                ("clMyRTCAREF_dMyZ", c_double),
                ("clMyRTCAREF_dMyStdX", c_double),
                ("clMyRTCAREF_dMyStdY", c_double),
                ("clMyRTCAREF_dMyStdZ", c_double),
                ("clMyRTCAREF_dMyStdXY", c_double),
                ("clMyRTCAREF_dMyStdYZ", c_double),
                ("clMyRTCAREF_dMyStdZX", c_double),
                ("clMyRTCAREF_fMyUndulation", c_float),
                ("clMyRTCAREF_ucMyNumSatsTracked", c_char),
                ("clMyRTCAREF_ucMyNumSatsInSol", c_char),
                ("clMyRTCAREF_ucMyNumHighSats", c_char),
                ("clMyRTCAREF_ucMyNumHighL2Sats", c_char),
                ("clMyRTCAREF_ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class MASTERPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("fFloat", c_float),
                ("fFloat", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ]


# noinspection PyTypeChecker
class ROVERPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("fFloat", c_float),
                ("fFloat", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ]


# noinspection PyTypeChecker
class HEADINGDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("fFloat", c_float),
                ("clMyHeadingInfo_fMyHeadingStdDev", c_float),
                ("clMyHeadingInfo_fMyPitchStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class RAWCNAVFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMyPrn", c_ulong),
                ("ulMyFrameId", c_ulong),
                ("aucMyRawFrameData", c_char*38),
                ]


# noinspection PyTypeChecker
class MARK1PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class MARK2PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class CONFIRMCODE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acConfirmationCode", c_char*80),
                ]


# noinspection PyTypeChecker
class MARK3TIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyWeek", c_long),
                ("dMySeconds", c_double),
                ("dMyOffset", c_double),
                ("dMyOffsetStd", c_double),
                ("dMyUTCOffset", c_double),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class MARK4TIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyWeek", c_long),
                ("dMySeconds", c_double),
                ("dMyOffset", c_double),
                ("dMyOffsetStd", c_double),
                ("dMyUTCOffset", c_double),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class MFGTESTRESULTS_MfgTestResultsList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMfgTestType", c_uint),
                ("eMyTestResult", c_uint),
                ("szMyResult", c_char*100),
                ]


# noinspection PyTypeChecker
class MFGTESTRESULTS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("MfgTestResultsList_arraylength", c_ulong),
                ("MfgTestResultsList", MFGTESTRESULTS_MfgTestResultsList*20),
                ]


# noinspection PyTypeChecker
class SIGNALCONFIGURATION_aclSigConfig(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignalType", c_uint),
                ("fMyPLLBandwidth", c_float),
                ("ulMyPLLAccumPeriodUS", c_ulong),
                ("ulMyDLLTimeConstSec", c_ulong),
                ("eMyCorrelatorType", c_uint),
                ]


# noinspection PyTypeChecker
class SIGNALCONFIGURATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclSigConfig_arraylength", c_ulong),
                ("aclSigConfig", SIGNALCONFIGURATION_aclSigConfig*60),
                ]


# noinspection PyTypeChecker
class PDPSTAT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyStatus_eMyStatus", c_uint),
                ("clMyStatus_eMyMode", c_uint),
                ("clMyStatus_eMyDynamics", c_uint),
                ("clMyStatus_uiNumPsrUsed", c_uint),
                ("clMyStatus_uiNumPhaseUsed", c_uint),
                ("clMyStatus_dMySecondsContRelOp", c_double),
                ("clMyStatus_dMyEstimatedNorthing900SecStdDev", c_double),
                ("clMyStatus_dMyEstimatedEasting900SecStdDev", c_double),
                ]


# noinspection PyTypeChecker
class MARK1COUNT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPeriod", c_ulong),
                ("usMyCount", c_ushort),
                ]


# noinspection PyTypeChecker
class MARK2COUNT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPeriod", c_ulong),
                ("usMyCount", c_ushort),
                ]


# noinspection PyTypeChecker
class MARK3COUNT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPeriod", c_ulong),
                ("usMyCount", c_ushort),
                ]


# noinspection PyTypeChecker
class MARK4COUNT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPeriod", c_ulong),
                ("usMyCount", c_ushort),
                ]


# noinspection PyTypeChecker
class RTCM1033(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_DescriptorCounter", c_char),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ("clMyRTCMV3REF_SerialNumberCounter", c_char),
                ("clMyRTCMV3REF_AntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaSerialNumber", c_char*31),
                ("clMyRTCMV3REF_ReceiverTypeDescriptorCounter", c_char),
                ("clMyRTCMV3REF_ReceiverTypeDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverTypeDescriptor", c_char*31),
                ("clMyRTCMV3REF_ReceiverFirmwareVersionCounter", c_char),
                ("clMyRTCMV3REF_ReceiverFirmwareVersion_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverFirmwareVersion", c_char*31),
                ("clMyRTCMV3REF_ReceiverSerialNumberCounter", c_char),
                ("clMyRTCMV3REF_ReceiverSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class RTCM1033IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_DescriptorCounter", c_char),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ("clMyRTCMV3REF_SerialNumberCounter", c_char),
                ("clMyRTCMV3REF_AntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaSerialNumber", c_char*31),
                ("clMyRTCMV3REF_ReceiverTypeDescriptorCounter", c_char),
                ("clMyRTCMV3REF_ReceiverTypeDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverTypeDescriptor", c_char*31),
                ("clMyRTCMV3REF_ReceiverFirmwareVersionCounter", c_char),
                ("clMyRTCMV3REF_ReceiverFirmwareVersion_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverFirmwareVersion", c_char*31),
                ("clMyRTCMV3REF_ReceiverSerialNumberCounter", c_char),
                ("clMyRTCMV3REF_ReceiverSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class RTCMDATA1033(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_ReferenceStationID", c_ushort),
                ("clMyRTCMV3REF_DescriptorCounter", c_char),
                ("clMyRTCMV3REF_AntennaDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaDescriptor", c_char*31),
                ("clMyRTCMV3REF_AntennaSetupID", c_char),
                ("clMyRTCMV3REF_SerialNumberCounter", c_char),
                ("clMyRTCMV3REF_AntennaSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_AntennaSerialNumber", c_char*31),
                ("clMyRTCMV3REF_ReceiverTypeDescriptorCounter", c_char),
                ("clMyRTCMV3REF_ReceiverTypeDescriptor_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverTypeDescriptor", c_char*31),
                ("clMyRTCMV3REF_ReceiverFirmwareVersionCounter", c_char),
                ("clMyRTCMV3REF_ReceiverFirmwareVersion_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverFirmwareVersion", c_char*31),
                ("clMyRTCMV3REF_ReceiverSerialNumberCounter", c_char),
                ("clMyRTCMV3REF_ReceiverSerialNumber_Len", c_ulong),
                ("clMyRTCMV3REF_ReceiverSerialNumber", c_char*31),
                ]


# noinspection PyTypeChecker
class DLLINFO_aclMyDLLInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("ulMyPeriodUS", c_ulong),
                ("dMyCodeError", c_double),
                ("dMyCodeCorr", c_double),
                ("fMyCodeLockPower", c_float),
                ("fMyCodeRate", c_float),
                ("fMyBandwidth", c_float),
                ("fMyK0", c_float),
                ("fMyK1", c_float),
                ]


# noinspection PyTypeChecker
class DLLINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDLLInfo_arraylength", c_ulong),
                ("aclMyDLLInfo", DLLINFO_aclMyDLLInfo*325),
                ]


# noinspection PyTypeChecker
class CHANRESETEVENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("ulMySatelliteID", c_ulong),
                ("eMyResetEvent", c_uint),
                ]


# noinspection PyTypeChecker
class PLLINFO_aclMyPLLInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("ulMyPeriodUS", c_ulong),
                ("fMyPhaseError", c_float),
                ("fMyPhaseErrorSum", c_float),
                ("fMyDoppler", c_float),
                ("fMyAcceleration", c_float),
                ("fMyBandwidth", c_float),
                ("fMyK0", c_float),
                ("fMyK1", c_float),
                ("fMyK2", c_float),
                ("eMyLoopType", c_uint),
                ]


# noinspection PyTypeChecker
class PLLINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyPLLInfo_arraylength", c_ulong),
                ("aclMyPLLInfo", PLLINFO_aclMyPLLInfo*325),
                ]


# noinspection PyTypeChecker
class MARK3PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class MARK4PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class GALALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatId", c_ulong),
                ("bMyFNAVReceived", c_bool),
                ("bMyINAVReceived", c_bool),
                ("ucMyE1BHealth", c_char),
                ("ucMyE5aHealth", c_char),
                ("ucMyE5bHealth", c_char),
                ("ucMyReserved1", c_char),
                ("ulMyIODa", c_ulong),
                ("clMyT0a_ulMyWeeks", c_ulong),
                ("clMyT0a_ulMyMilliseconds", c_ulong),
                ("dMyEcc", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmega", c_double),
                ("dMyM0", c_double),
                ("dMyAf0", c_double),
                ("dMyAf1", c_double),
                ("dMyDeltaRootA", c_double),
                ("dMyDeltaI", c_double),
                ]


# noinspection PyTypeChecker
class GALCLOCK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyA0", c_double),
                ("dMyA1", c_double),
                ("lMyDeltaTls", c_long),
                ("ulMyTot", c_ulong),
                ("ulMyWNt", c_ulong),
                ("ulMyWNlsf", c_ulong),
                ("ulMyDN", c_ulong),
                ("lMyDeltaTlsf", c_long),
                ("dMyA0g", c_double),
                ("dMyA1g", c_double),
                ("ulMyT0g", c_ulong),
                ("ulMyWN0g", c_ulong),
                ]


# noinspection PyTypeChecker
class GALEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatId", c_ulong),
                ("bMyFNAVReceived", c_bool),
                ("bMyINAVReceived", c_bool),
                ("ucMyE1BHealth", c_char),
                ("ucMyE5aHealth", c_char),
                ("ucMyE5bHealth", c_char),
                ("ucMyE1BDVS", c_char),
                ("ucMyE5aDVS", c_char),
                ("ucMyE5bDVS", c_char),
                ("ucMyINAVSISA", c_char),
                ("ucMyReserved1", c_char),
                ("ulMyIODNav", c_ulong),
                ("ulMyT0e", c_ulong),
                ("dMyRootA", c_double),
                ("dMyDeltaN", c_double),
                ("dMyM0", c_double),
                ("dMyEcc", c_double),
                ("dMyOmega", c_double),
                ("dMyCuc", c_double),
                ("dMyCus", c_double),
                ("dMyCrc", c_double),
                ("dMyCrs", c_double),
                ("dMyCic", c_double),
                ("dMyCis", c_double),
                ("dMyI0", c_double),
                ("dMyIDot", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmegaDot", c_double),
                ("ulMyFNAVT0c", c_ulong),
                ("dMyFNAVAf0", c_double),
                ("dMyFNAVAf1", c_double),
                ("dMyFNAVAf2", c_double),
                ("ulMyINAVT0c", c_ulong),
                ("dMyINAVAf0", c_double),
                ("dMyINAVAf1", c_double),
                ("dMyINAVAf2", c_double),
                ("dMyE1E5aBGD", c_double),
                ("dMyE1E5bBGD", c_double),
                ]


# noinspection PyTypeChecker
class GALFNAVRAWALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyIODa", c_ulong),
                ("ulMyWNa", c_ulong),
                ("ulMyT0a", c_ulong),
                ("aucMyRawData", c_char*20),
                ]


# noinspection PyTypeChecker
class GALFNAVRAWEPHEMERIS_aclMyRawPages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyPage", c_char*27),
                ("ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class GALFNAVRAWEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatId", c_ulong),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyRawPages_arraylength", c_ulong),
                ("aclMyRawPages", GALFNAVRAWEPHEMERIS_aclMyRawPages*4),
                ]


# noinspection PyTypeChecker
class GALINAVRAWALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyIODa", c_ulong),
                ("ulMyWNa", c_ulong),
                ("ulMyT0a", c_ulong),
                ("aucMyRawData", c_char*20),
                ]


# noinspection PyTypeChecker
class GALINAVRAWEPHEMERIS_aclMyRawWords(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyWord", c_char*16),
                ]


# noinspection PyTypeChecker
class GALINAVRAWEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatId", c_ulong),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyRawWords_arraylength", c_ulong),
                ("aclMyRawWords", GALINAVRAWEPHEMERIS_aclMyRawWords*6),
                ]


# noinspection PyTypeChecker
class GALIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyAi0", c_double),
                ("dMyAi1", c_double),
                ("dMyAi2", c_double),
                ("ucMySF1", c_char),
                ("ucMySF2", c_char),
                ("ucMySF3", c_char),
                ("ucMySF4", c_char),
                ("ucMySF5", c_char),
                ]


# noinspection PyTypeChecker
class MARK1TIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyWeek", c_long),
                ("dMySeconds", c_double),
                ("dMyOffset", c_double),
                ("dMyOffsetStd", c_double),
                ("dMyUTCOffset", c_double),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class BASEANTENNAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySourceMessage", c_ulong),
                ("acMyStationID", c_char*4),
                ("szMyModelName", c_char*32),
                ("szMySerialNumber", c_char*32),
                ("ulMySetupID", c_ulong),
                ]


# noinspection PyTypeChecker
class HEADINGEXT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeadingExtInfo_ucMySolutionStatus", c_char),
                ("clMyHeadingExtInfo_ucMySolutionType", c_char),
                ("clMyHeadingExtInfo_fMyHeadingOffset", c_float),
                ("clMyHeadingExtInfo_fMyPitchOffset", c_float),
                ("clMyHeadingExtInfo_dMyX", c_double),
                ("clMyHeadingExtInfo_dMyY", c_double),
                ("clMyHeadingExtInfo_dMyZ", c_double),
                ("clMyHeadingExtInfo_dMyXVar", c_double),
                ("clMyHeadingExtInfo_dMyYVar", c_double),
                ("clMyHeadingExtInfo_dMyZVar", c_double),
                ("clMyHeadingExtInfo_dMyXYVar", c_double),
                ("clMyHeadingExtInfo_dMyYZVar", c_double),
                ("clMyHeadingExtInfo_dMyZXVar", c_double),
                ("clMyHeadingExtInfo_acMyMasterId", c_char*4),
                ("clMyHeadingExtInfo_acMyRoverId", c_char*4),
                ("clMyHeadingExtInfo_fMyUndulation", c_float),
                ("clMyHeadingExtInfo_ucMyNumSatsTracked", c_char),
                ("clMyHeadingExtInfo_ucMyNumSatsInSol", c_char),
                ("clMyHeadingExtInfo_ucMyNumHighSats", c_char),
                ("clMyHeadingExtInfo_ucMyNumHighL2Sats", c_char),
                ("clMyHeadingExtInfo_ucMyExtendedSolutionStatus", c_char),
                ("clMyHeadingExtInfo_ucMyGPSandGLOFreqsInSol", c_char),
                ]


# noinspection PyTypeChecker
class HEADINGEXTIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeadingExtInfo_ucMySolutionStatus", c_char),
                ("clMyHeadingExtInfo_ucMySolutionType", c_char),
                ("clMyHeadingExtInfo_fMyHeadingOffset", c_float),
                ("clMyHeadingExtInfo_fMyPitchOffset", c_float),
                ("clMyHeadingExtInfo_dMyX", c_double),
                ("clMyHeadingExtInfo_dMyY", c_double),
                ("clMyHeadingExtInfo_dMyZ", c_double),
                ("clMyHeadingExtInfo_dMyXVar", c_double),
                ("clMyHeadingExtInfo_dMyYVar", c_double),
                ("clMyHeadingExtInfo_dMyZVar", c_double),
                ("clMyHeadingExtInfo_dMyXYVar", c_double),
                ("clMyHeadingExtInfo_dMyYZVar", c_double),
                ("clMyHeadingExtInfo_dMyZXVar", c_double),
                ("clMyHeadingExtInfo_acMyMasterId", c_char*4),
                ("clMyHeadingExtInfo_acMyRoverId", c_char*4),
                ("clMyHeadingExtInfo_fMyUndulation", c_float),
                ("clMyHeadingExtInfo_ucMyNumSatsTracked", c_char),
                ("clMyHeadingExtInfo_ucMyNumSatsInSol", c_char),
                ("clMyHeadingExtInfo_ucMyNumHighSats", c_char),
                ("clMyHeadingExtInfo_ucMyNumHighL2Sats", c_char),
                ("clMyHeadingExtInfo_ucMyExtendedSolutionStatus", c_char),
                ("clMyHeadingExtInfo_ucMyGPSandGLOFreqsInSol", c_char),
                ]


# noinspection PyTypeChecker
class GIOVEFNAVRAWFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMySatId", c_ulong),
                ("ulMyFrameId", c_ulong),
                ("clMyRawFrameData_aucMyPage", c_char*100),
                ]


# noinspection PyTypeChecker
class GIOVEINAVRAWFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMySatId", c_ulong),
                ("ulMyFrameId", c_ulong),
                ("eMySignalType", c_uint),
                ("clMyRawFrameData_aucMyPage", c_char*100),
                ]


# noinspection PyTypeChecker
class GIOVEFNAVRAWEPHEMERIS_aclMyRawPages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyPage", c_char*100),
                ]


# noinspection PyTypeChecker
class GIOVEFNAVRAWEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatId", c_ulong),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyRawPages_arraylength", c_ulong),
                ("aclMyRawPages", GIOVEFNAVRAWEPHEMERIS_aclMyRawPages*4),
                ]


# noinspection PyTypeChecker
class GIOVEFNAVRAWALMANAC_aclMyRawPages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyPage", c_char*100),
                ]


# noinspection PyTypeChecker
class GIOVEFNAVRAWALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyRawPages_arraylength", c_ulong),
                ("aclMyRawPages", GIOVEFNAVRAWALMANAC_aclMyRawPages*12),
                ]


# noinspection PyTypeChecker
class GIOVEINAVRAWEPHEMERIS_aclMyRawPages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyPage", c_char*100),
                ]


# noinspection PyTypeChecker
class GIOVEINAVRAWEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatId", c_ulong),
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyRawPages_arraylength", c_ulong),
                ("aclMyRawPages", GIOVEINAVRAWEPHEMERIS_aclMyRawPages*12),
                ]


# noinspection PyTypeChecker
class GIOVEINAVRAWALMANAC_aclMyRawPages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyPage", c_char*100),
                ]


# noinspection PyTypeChecker
class GIOVEINAVRAWALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyReceiveTime_ulMyWeeks", c_ulong),
                ("clMyReceiveTime_ulMyMilliseconds", c_ulong),
                ("aclMyRawPages_arraylength", c_ulong),
                ("aclMyRawPages", GIOVEINAVRAWALMANAC_aclMyRawPages*42),
                ]


# noinspection PyTypeChecker
class OUTPUTUNDULATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyUndulationData_eMyUndulationType", c_uint),
                ("clMyUndulationData_fMyUndulation", c_float),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_dMyHeight", c_double),
                ]


# noinspection PyTypeChecker
class LOGFILESTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFileState", c_uint),
                ("szMyFileName", c_char*128),
                ("ulMyFileSize", c_ulong),
                ("eMyStorageMedium", c_uint),
                ("ulMyMediaFreeSpace", c_ulong),
                ("ulMyMediaCapacity", c_ulong),
                ]


# noinspection PyTypeChecker
class CHANCONFIGLIST_clChanCfgListSysArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulNumChans", c_ulong),
                ("eSignalType", c_uint),
                ]


# noinspection PyTypeChecker
class CHANCONFIGLIST_ChanCfgListArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clChanCfgListSysArray_arraylength", c_ulong),
                ("clChanCfgListSysArray", CHANCONFIGLIST_clChanCfgListSysArray*16),
                ]


# noinspection PyTypeChecker
class CHANCONFIGLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("SetInUse", c_ulong),
                ("ChanCfgListArray_arraylength", c_ulong),
                ("ChanCfgListArray", CHANCONFIGLIST_ChanCfgListArray*20),
                ]


# noinspection PyTypeChecker
class RTCMDATAV3USER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3User_MessageNumber", c_ushort),
                ("clMyRTCMV3User_Reserved", c_char),
                ("clMyRTCMV3User_Message4093Subtype", c_char),
                ("clMyRTCMV3User_UserDefinedData_Len", c_ulong),
                ("clMyRTCMV3User_UserDefinedData", c_char*200),
                ]


# noinspection PyTypeChecker
class RTCMV3USER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3User_MessageNumber", c_ushort),
                ("clMyRTCMV3User_Reserved", c_char),
                ("clMyRTCMV3User_Message4093Subtype", c_char),
                ("clMyRTCMV3User_UserDefinedData_Len", c_ulong),
                ("clMyRTCMV3User_UserDefinedData", c_char*200),
                ]


# noinspection PyTypeChecker
class RTCMV3USERDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3User_UserDefinedData_Len", c_ulong),
                ("clMyRTCMV3User_UserDefinedData", c_char*200),
                ]


# noinspection PyTypeChecker
class RTCMV3USERIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3User_MessageNumber", c_ushort),
                ("clMyRTCMV3User_Reserved", c_char),
                ("clMyRTCMV3User_Message4093Subtype", c_char),
                ("clMyRTCMV3User_UserDefinedData_Len", c_ulong),
                ("clMyRTCMV3User_UserDefinedData", c_char*200),
                ]


# noinspection PyTypeChecker
class SBASCORRECTIONS_aclMyCorrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyIODE", c_ulong),
                ("ulMyIODP", c_ulong),
                ("clMyOrbitCorrection_dMyX", c_double),
                ("clMyOrbitCorrection_dMyY", c_double),
                ("clMyOrbitCorrection_dMyZ", c_double),
                ("dMySlowClockCorrection", c_double),
                ("dMyFastClockCorrection", c_double),
                ("dMyCorrectionVariance", c_double),
                ]


# noinspection PyTypeChecker
class SBASCORRECTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_ulMySourcePRN", c_ulong),
                ("clMyInfo_eMyServiceProvider", c_uint),
                ("clMyTimeOfNewestCorrection_clMyInfo_ulMyWeeks", c_ulong),
                ("clMyTimeOfNewestCorrection_clMyInfo_ulMyMilliseconds", c_ulong),
                ("aclMyCorrections_arraylength", c_ulong),
                ("aclMyCorrections", SBASCORRECTIONS_aclMyCorrections*318),
                ]


# noinspection PyTypeChecker
class HASSSTATUS_aMyHLASSPosPoly(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("eMySystemVariant", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyIOD", c_ulong),
                ("bMyIsPolyComputable", c_bool),
                ("clMyReferenceTime_ulMyWeeks", c_ulong),
                ("clMyReferenceTime_ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class HASSSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aMyHLASSPosPoly_arraylength", c_ulong),
                ("aMyHLASSPosPoly", HASSSTATUS_aMyHLASSPosPoly*319),
                ]


# noinspection PyTypeChecker
class LASSSTATUS_aMyHLASSPosPoly(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("eMySystemVariant", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyIOD", c_ulong),
                ("bMyIsPolyComputable", c_bool),
                ("clMyReferenceTime_ulMyWeeks", c_ulong),
                ("clMyReferenceTime_ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class LASSSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aMyHLASSPosPoly_arraylength", c_ulong),
                ("aMyHLASSPosPoly", LASSSTATUS_aMyHLASSPosPoly*318),
                ]


# noinspection PyTypeChecker
class RANGECORRECTIONS_aclMyCorrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("clMyPositionPolynomial_clMyData_ulMyIOD", c_ulong),
                ("clMyData_fMyTotalCorrection", c_float),
                ("clMyData_fMyTotalCorrectionVariance", c_float),
                ("clMyData_fMyIonoCorrection", c_float),
                ]


# noinspection PyTypeChecker
class RANGECORRECTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_eMyType", c_uint),
                ("clMyInfo_acMyStationID", c_char*4),
                ("clMyTimeOfNewestCorrection_clMyInfo_ulMyWeeks", c_ulong),
                ("clMyTimeOfNewestCorrection_clMyInfo_ulMyMilliseconds", c_ulong),
                ("aclMyCorrections_arraylength", c_ulong),
                ("aclMyCorrections", RANGECORRECTIONS_aclMyCorrections*72),
                ]


# noinspection PyTypeChecker
class CLOCKSTEERINGADJUSTMENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyTime_ulMyWeeks", c_ulong),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ("eMyType", c_uint),
                ("dMyAdjustAmount", c_double),
                ("dMyAdjustDriftAmount", c_double),
                ("dMyAdjustDriftVarAmount", c_double),
                ]


# noinspection PyTypeChecker
class PACKAGEDOBSERVATIONS_aclMyObservationSets(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_clMyPositionPolynomial_eMySystemType", c_uint),
                ("clMyID_clMyPositionPolynomial_idMyID", satelliteid),
                ("clMyPositionPolynomial_ulMyIOD", c_ulong),
                ("clMyIonoTropoEntry_bMyHasTropoCorr", c_bool),
                ("clMyIonoTropoEntry_bMyHasKlobucharIonoCorr", c_bool),
                ("clMyIonoTropoEntry_bMyHasDualFreqIonoCorr", c_bool),
                ("clMyIonoTropoEntry_bMyHasGridIonoCorr", c_bool),
                ("bMySBASCorrectionIsValid", c_bool),
                ("bMyRangeCorrectionIsValid", c_bool),
                ("clMyPositionPolynomial_clMyRangeCorrection_ulMyIOD", c_ulong),
                ("bMyAzimuthAndElevationAreValid", c_bool),
                ("fMyAzimuth", c_float),
                ("fMyElevation", c_float),
                ]


# noinspection PyTypeChecker
class PACKAGEDOBSERVATIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyObservationSets_arraylength", c_ulong),
                ("aclMyObservationSets", PACKAGEDOBSERVATIONS_aclMyObservationSets*72),
                ]


# noinspection PyTypeChecker
class PSRSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class PSRSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", PSRSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class PSRDOP2_clMyDOPs_aclMyTDOPs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("fMyDOP", c_float),
                ]


# noinspection PyTypeChecker
class PSRDOP2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyVDOP", c_float),
                ("clMyDOPs_aclMyTDOPs_arraylength", c_ulong),
                ("clMyDOPs_aclMyTDOPs", PSRDOP2_clMyDOPs_aclMyTDOPs*5),
                ]


# noinspection PyTypeChecker
class PSRTIME2_clMySystemTimeOffsets_aclMySystemOffsets(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("dMyBias", c_double),
                ("dMyBiasStdDev", c_double),
                ("dMyRate", c_double),
                ("dMyRateStdDev", c_double),
                ]


# noinspection PyTypeChecker
class PSRTIME2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySystemTimeOffsets_aclMySystemOffsets_arraylength", c_ulong),
                ("clMySystemTimeOffsets_aclMySystemOffsets", PSRTIME2_clMySystemTimeOffsets_aclMySystemOffsets*5),
                ]


# noinspection PyTypeChecker
class PROPAGATEDCLOCKMODEL2_aclMySystemBiases(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("dMyBias", c_double),
                ("dMyBiasStdDev", c_double),
                ("dMyRate", c_double),
                ("dMyRateStdDev", c_double),
                ]


# noinspection PyTypeChecker
class PROPAGATEDCLOCKMODEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("aclMySystemBiases_arraylength", c_ulong),
                ("aclMySystemBiases", PROPAGATEDCLOCKMODEL2_aclMySystemBiases*5),
                ]


# noinspection PyTypeChecker
class CLOCKMODEL2_aclMySystemBiases(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("dMyBias", c_double),
                ("dMyBiasStdDev", c_double),
                ]


# noinspection PyTypeChecker
class CLOCKMODEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("dMyRate", c_double),
                ("aclMySystemBiases_arraylength", c_ulong),
                ("aclMySystemBiases", CLOCKMODEL2_aclMySystemBiases*5),
                ]


# noinspection PyTypeChecker
class PSRCHANNELSTATUS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("sigMyChannel", c_ulong),
                ("eMyStatus", c_uint),
                ("dMyObsStdDev", c_double),
                ("dMyResidual", c_double),
                ]


# noinspection PyTypeChecker
class PSRCHANNELSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", PSRCHANNELSTATUS_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class RTKDOP2_clMyDOPs_aclMyTDOPs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("fMyDOP", c_float),
                ]


# noinspection PyTypeChecker
class RTKDOP2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyVDOP", c_float),
                ("clMyDOPs_aclMyTDOPs_arraylength", c_ulong),
                ("clMyDOPs_aclMyTDOPs", RTKDOP2_clMyDOPs_aclMyTDOPs*5),
                ]


# noinspection PyTypeChecker
class SBASFAST_aclMyFast(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPRN", c_ushort),
                ("clMyTime_ulMyWeeks", c_ulong),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ("ulMyUDRE", c_ulong),
                ]


# noinspection PyTypeChecker
class SBASFAST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySourceSystemVariant", c_uint),
                ("ulMySourcePrn", c_ulong),
                ("clMyLatestFastTime_ulMyWeeks", c_ulong),
                ("clMyLatestFastTime_ulMyMilliseconds", c_ulong),
                ("dMyFastTimeOut", c_double),
                ("aclMyFast_arraylength", c_ulong),
                ("aclMyFast", SBASFAST_aclMyFast*51),
                ]


# noinspection PyTypeChecker
class RTKSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class RTKSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", RTKSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class MATCHEDSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class MATCHEDSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", MATCHEDSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class PASHR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_clMyPVASolution_eMyPositionType", c_uint),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyCovariance_clMyAttitude_clMyPVASolution_adMyElements", c_double*9),
                ("clMyHeaveInfo_dMyHeave", c_double),
                ]


# noinspection PyTypeChecker
class PSRINTEGRITYEVENT_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("dMyResidual", c_double),
                ("dMyResidualVariance", c_double),
                ]


# noinspection PyTypeChecker
class PSRINTEGRITYEVENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyRedundancy", c_ulong),
                ("dMyDesiredGlobalThreshold", c_double),
                ("dMyRequiredGlobalThreshold", c_double),
                ("dMyGlobalStatistic", c_double),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", PSRINTEGRITYEVENT_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class DEBUGETHER_clMyDebugEtherBase_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPacketPointer", c_ulong),
                ("dMyTime", c_double),
                ("ulMyTaskID", c_ulong),
                ("szMyTaskName", c_char*51),
                ]


# noinspection PyTypeChecker
class DEBUGETHER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDebugEtherBase_ulMyEtherNum", c_ulong),
                ("clMyDebugEtherBase_szMyEtherName", c_char*51),
                ("clMyDebugEtherBase_ulMyNumPackets", c_ulong),
                ("clMyDebugEtherBase_ulMyPacketCap", c_ulong),
                ("clMyDebugEtherBase_aclMyEntries_arraylength", c_ulong),
                ("clMyDebugEtherBase_aclMyEntries", DEBUGETHER_clMyDebugEtherBase_aclMyEntries*30),
                ]


# noinspection PyTypeChecker
class DEBUGETHEREXCEEDED_clMyDebugEtherBase_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPacketPointer", c_ulong),
                ("dMyTime", c_double),
                ("ulMyTaskID", c_ulong),
                ("szMyTaskName", c_char*51),
                ]


# noinspection PyTypeChecker
class DEBUGETHEREXCEEDED(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDebugEtherBase_ulMyEtherNum", c_ulong),
                ("clMyDebugEtherBase_szMyEtherName", c_char*51),
                ("clMyDebugEtherBase_ulMyNumPackets", c_ulong),
                ("clMyDebugEtherBase_ulMyPacketCap", c_ulong),
                ("clMyDebugEtherBase_aclMyEntries_arraylength", c_ulong),
                ("clMyDebugEtherBase_aclMyEntries", DEBUGETHEREXCEEDED_clMyDebugEtherBase_aclMyEntries*30),
                ]


# noinspection PyTypeChecker
class SBASMASK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyTime_clMyMask_ulMyWeeks", c_ulong),
                ("clMyTime_clMyMask_ulMyMilliseconds", c_ulong),
                ("clMyMask_ulMyIODP", c_ulong),
                ("clMyMask_ulMyNumSats", c_ulong),
                ("clMyMask_aulMyPrnToSlot", c_ulong*202),
                ]


# noinspection PyTypeChecker
class DEBUGCHANMAP_aclMySigChanMaps(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("svMyChan", c_ulong),
                ("ulMyIDNumber", c_ulong),
                ("sigMyChan", c_ulong),
                ("ulMyMinosChan", c_ulong),
                ("idMySatID", satelliteid),
                ("eMySignalType", c_uint),
                ("ulMyAssignID", c_ulong),
                ("eMyChannelType", c_uint),
                ]


# noinspection PyTypeChecker
class DEBUGCHANMAP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyChannelConfigurationMode", c_uint),
                ("aclMySigChanMaps_arraylength", c_ulong),
                ("aclMySigChanMaps", DEBUGCHANMAP_aclMySigChanMaps*500),
                ]


# noinspection PyTypeChecker
class ELEVCUTOFFDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyElevationCutoffAngle", c_float),
                ("fMyElevationCutoffAngle", c_float),
                ]


# noinspection PyTypeChecker
class SIMULATEDOBSERRORS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignalType", c_uint),
                ("ulMyID", c_ulong),
                ("eMyObservationType", c_uint),
                ("dMyError", c_double),
                ]


# noinspection PyTypeChecker
class SIMULATEDOBSERRORS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", SIMULATEDOBSERRORS_aclMyEntries*872),
                ]


# noinspection PyTypeChecker
class SIMULATEOBSERRORSTATUS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignalType", c_uint),
                ("ulMyID", c_ulong),
                ("eMyObservationType", c_uint),
                ("clMyTime_ulMyWeeks", c_ulong),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ("dMyDuration", c_double),
                ("eMyErrorType", c_uint),
                ]


# noinspection PyTypeChecker
class SIMULATEOBSERRORSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", SIMULATEOBSERRORSTATUS_aclMyEntries*872),
                ]


# noinspection PyTypeChecker
class SBASSLOW_aclMySlow(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyPRN", c_ushort),
                ("clMyTime_ulMyWeeks", c_ulong),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ("ulMyIODE", c_ulong),
                ("adMyXYZ", c_double*3),
                ]


# noinspection PyTypeChecker
class SBASSLOW(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySourceSystemVariant", c_uint),
                ("ulMySourcePrn", c_ulong),
                ("aclMySlow_arraylength", c_ulong),
                ("aclMySlow", SBASSLOW_aclMySlow*51),
                ]


# noinspection PyTypeChecker
class RAWLBANDCOMDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*32),
                ]


# noinspection PyTypeChecker
class GRIDIONO_aclMyIonoCorrs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyDelay", c_float),
                ("fMyVariance", c_float),
                ]


# noinspection PyTypeChecker
class GRIDIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySourcePRN", c_ulong),
                ("bMyReceiverIsInGrid", c_bool),
                ("aclMyIonoCorrs_arraylength", c_ulong),
                ("aclMyIonoCorrs", GRIDIONO_aclMyIonoCorrs*72),
                ]


# noinspection PyTypeChecker
class GPGSTDATA_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("dMyObsStdDev", c_double),
                ]


# noinspection PyTypeChecker
class GPGSTDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCovariance_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_adMyElements", c_double*9),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", GPGSTDATA_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class BESTSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class BESTSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", BESTSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class PSRRESIDUALS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("dMyResidual", c_double),
                ("dMyResidualStdDev", c_double),
                ]


# noinspection PyTypeChecker
class PSRRESIDUALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", PSRRESIDUALS_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class LBANDTRACKSTAT_aclMyLBandChanStates(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyBeamName", c_char*8),
                ("ulMyAssignedFrequency", c_ulong),
                ("usMyBaudRate", c_ushort),
                ("usMyServiceID", c_ushort),
                ("usMyTrackingStatus", c_ushort),
                ("usMyReserved", c_ushort),
                ("fMyDoppler", c_float),
                ("fMyCN0", c_float),
                ("fMyPhaseStdDev", c_float),
                ("fMyLockTime", c_float),
                ("ulMyTotalUniqueWordBits", c_ulong),
                ("ulMyBadUniqueWordBits", c_ulong),
                ("ulMyBadUniqueWords", c_ulong),
                ("ulMyTotalViterbiSymbols", c_ulong),
                ("ulMyCorrectedViterbiSyms", c_ulong),
                ("fMyBER", c_float),
                ]


# noinspection PyTypeChecker
class LBANDTRACKSTAT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyLBandChanStates_arraylength", c_ulong),
                ("aclMyLBandChanStates", LBANDTRACKSTAT_aclMyLBandChanStates*5),
                ]


# noinspection PyTypeChecker
class IONOTROPO2_aclMyIonoTropo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyTropoCorr", c_float),
                ("fMyTropoCorrVar", c_float),
                ("bMyHasTropoCorr", c_bool),
                ("fMyDualFreqIonoCorr", c_float),
                ("fMyDualFreqIonoCorrVar", c_float),
                ("bMyHasDualFreqIonoCorr", c_bool),
                ("fMyGridIonoCorr", c_float),
                ("fMyGridIonoCorrVar", c_float),
                ("bMyHasGridIonoCorr", c_bool),
                ("fMyKlobucharIonoCorr", c_float),
                ("fMyKlobucharIonoCorrVar", c_float),
                ("bMyHasKlobucharIonoCorr", c_bool),
                ]


# noinspection PyTypeChecker
class IONOTROPO2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_bMyKlobucharModelIsDefault", c_bool),
                ("clMyInfo_ulMyKlobucharIODI", c_ulong),
                ("aclMyIonoTropo_arraylength", c_ulong),
                ("aclMyIonoTropo", IONOTROPO2_aclMyIonoTropo*72),
                ]


# noinspection PyTypeChecker
class TILTDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStatus", c_ulong),
                ("dMyXAccel", c_double),
                ("dMyYAccel", c_double),
                ("dMyAvgXIncl", c_double),
                ("dMyXIncl", c_double),
                ("dMyYIncl", c_double),
                ("dMyAvgYIncl", c_double),
                ("ulULONG", c_ulong),
                ]


# noinspection PyTypeChecker
class GPVTGDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyType", c_uint),
                ("eMyStatus", c_uint),
                ("clMyVelocity_dMyGroundTrack", c_double),
                ("clMyVelocity_dMyHorizontalSpeed", c_double),
                ("clMySolutionSatelliteInfo_ucMySystemSet", c_char),
                ("fMyDeclination", c_float),
                ("eMyNMEAVersion", c_uint),
                ]


# noinspection PyTypeChecker
class MAGNETICDECLINATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyDeclination", c_float),
                ("fMyDeclinationStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PSRVEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("cCharAsInt", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class GPRMCDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCMonth", c_char),
                ("ulUTCYear", c_ulong),
                ("UTCTimeStatus", c_uint),
                ("fMyDeclination", c_float),
                ("eMyEnableGPRMCAltitude", c_uint),
                ("eMyNMEATime", c_uint),
                ]


# noinspection PyTypeChecker
class RTKVEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("cCharAsInt", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class BESTVEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("cCharAsInt", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PDPVEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("cCharAsInt", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PDPSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class PDPSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", PDPSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class SOFTLOADSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class SOFTLOADDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyDebugString", c_char*255),
                ]


# noinspection PyTypeChecker
class DEBUGIQDATA_aclMyIQAccums(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lCarrierAccumI", c_long),
                ("lCarrierAccumQ", c_long),
                ("lCodeAccumI", c_long),
                ("lCodeAccumQ", c_long),
                ("lPunctualAccumI", c_long),
                ("lPunctualAccumQ", c_long),
                ("lWeight1I", c_long),
                ("lWeight1Q", c_long),
                ]


# noinspection PyTypeChecker
class DEBUGIQDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("ulMySatelliteID", c_ulong),
                ("eMyIQType", c_uint),
                ("aclMyIQAccums_arraylength", c_ulong),
                ("aclMyIQAccums", DEBUGIQDATA_aclMyIQAccums*25),
                ]


# noinspection PyTypeChecker
class BESTLEVERARM2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLeverArm_adMyInput", c_double*3),
                ("clMyLeverArm_adMyInputStdev", c_double*3),
                ("iMyMapping", c_int),
                ]


# noinspection PyTypeChecker
class TAGGEDMARK1PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyPVASolution_ulMyTagID", c_ulong),
                ]


# noinspection PyTypeChecker
class TAGGEDMARK2PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyPVASolution_ulMyTagID", c_ulong),
                ]


# noinspection PyTypeChecker
class GPGRSDATA_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("dMyResidual", c_double),
                ]


# noinspection PyTypeChecker
class GPGRSDATA_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class GPGRSDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", GPGRSDATA_aclMyEntries*325),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", GPGRSDATA_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ("eMyNMEAVersion", c_uint),
                ("eMyIncludeSBAS", c_uint),
                ("eMySource", c_uint),
                ]


# noinspection PyTypeChecker
class DEBUGBUFFER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySeqNo", c_ulong),
                ("szMyMessage", c_char*198),
                ]


# noinspection PyTypeChecker
class RXSTATUSUPDATE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyRxStatus", c_uint),
                ("eMyRxStatusFlag", c_uint),
                ("eMyRxStatusAuxiliary", c_uint),
                ]


# noinspection PyTypeChecker
class DDCDEBUG_aclMyDDCs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyEncoder", c_ulong),
                ("fMyNoiseFloor", c_float),
                ("ulMyDDCBottomBit", c_ulong),
                ("ulMyFinalRangeBottomBit", c_ulong),
                ("fMyDCOffset", c_float),
                ("fMyPDFError", c_float),
                ("afMyPDF_Len", c_ulong),
                ("afMyPDF", c_float*64),
                ]


# noinspection PyTypeChecker
class DDCDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDDCs_arraylength", c_ulong),
                ("aclMyDDCs", DDCDEBUG_aclMyDDCs*24),
                ]


# noinspection PyTypeChecker
class IMUTOANTOFFSETS_aclMyLeverArm(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOffset", c_uint),
                ("clMyEnclosure_afMyElements", c_float*3),
                ("clMyEnclosureStdev_afMyElements", c_float*3),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class IMUTOANTOFFSETS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iMyMapping", c_int),
                ("aclMyLeverArm_arraylength", c_ulong),
                ("aclMyLeverArm", IMUTOANTOFFSETS_aclMyLeverArm*3),
                ]


# noinspection PyTypeChecker
class BASEIONO_aclMyIonoCorrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteID_eMySystemType", c_uint),
                ("clMySatelliteID_idMyID", satelliteid),
                ("fMyIonoDelay", c_float),
                ("fMyIonoDelayRate", c_float),
                ]


# noinspection PyTypeChecker
class BASEIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDGPSType", c_uint),
                ("ulMyType", c_ulong),
                ("aclMyIonoCorrections_arraylength", c_ulong),
                ("aclMyIonoCorrections", BASEIONO_aclMyIonoCorrections*325),
                ]


# noinspection PyTypeChecker
class RANGECMP2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyRangeData_Len", c_ulong),
                ("aucMyRangeData", c_char*7800),
                ]


# noinspection PyTypeChecker
class RAIMSTATUS_aclMyRejectedSVs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("idMyID", satelliteid),
                ]


# noinspection PyTypeChecker
class RAIMSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMode", c_uint),
                ("eMyIntegrityStatus", c_uint),
                ("eMyHPLStatus", c_uint),
                ("dMyHPL", c_double),
                ("eMyVPLStatus", c_uint),
                ("dMyVPL", c_double),
                ("aclMyRejectedSVs_arraylength", c_ulong),
                ("aclMyRejectedSVs", RAIMSTATUS_aclMyRejectedSVs*20),
                ]


# noinspection PyTypeChecker
class ETHSTATUS_aclMyEthStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyInterface", c_uint),
                ("sMyMACAddress", c_char*18),
                ("eMyInterfaceConfig", c_uint),
                ]


# noinspection PyTypeChecker
class ETHSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEthStatus_arraylength", c_ulong),
                ("aclMyEthStatus", ETHSTATUS_aclMyEthStatus*2),
                ]


# noinspection PyTypeChecker
class IPSTATUS_aclMyIPStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyInterface", c_uint),
                ("sMyIPAddress", c_char*16),
                ("sMyNetmask", c_char*16),
                ("sMyGateway", c_char*16),
                ]


# noinspection PyTypeChecker
class IPSTATUS_aclMyDNSServer(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sIPAddress", c_char*16),
                ]


# noinspection PyTypeChecker
class IPSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyIPStatus_arraylength", c_ulong),
                ("aclMyIPStatus", IPSTATUS_aclMyIPStatus*4),
                ("aclMyDNSServer_arraylength", c_ulong),
                ("aclMyDNSServer", IPSTATUS_aclMyDNSServer*4),
                ]


# noinspection PyTypeChecker
class IMURATEPVAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class FRONTENDDATA_aclMyAGCFrontEndData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyFrontEnd", c_ulong),
                ("ulMyTimeStamp", c_ulong),
                ("bMyCalibrated", c_bool),
                ("ulMyAdjustMode", c_ulong),
                ("ulMyAdjustRate", c_ulong),
                ("ulMyPulseWidth", c_ulong),
                ("ulMyModulus", c_ulong),
                ("ulMyADCBottomBit", c_ulong),
                ("dMyDCOffset", c_double),
                ("dMyPDFError", c_double),
                ("adMyPDF", c_double*6),
                ]


# noinspection PyTypeChecker
class FRONTENDDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyAGCFrontEndData_arraylength", c_ulong),
                ("aclMyAGCFrontEndData", FRONTENDDATA_aclMyAGCFrontEndData*10),
                ]


# noinspection PyTypeChecker
class DEBUGBUFFERCMP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySeqNo", c_ulong),
                ("szMyMessage", c_char*198),
                ]


# noinspection PyTypeChecker
class DEBUGETHERREQUESTORS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPeriod", c_ulong),
                ("ulMyTrigger", c_ulong),
                ("ulMyTaskID", c_ulong),
                ("szMyTaskName", c_char*51),
                ]


# noinspection PyTypeChecker
class DEBUGETHERREQUESTORS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyEtherNum", c_ulong),
                ("szMyEtherName", c_char*51),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", DEBUGETHERREQUESTORS_aclMyEntries*30),
                ]


# noinspection PyTypeChecker
class GALINAVEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyParameters_ulMySatId", c_ulong),
                ("clMyParameters_ucMyE5bHealth", c_char),
                ("clMyParameters_ucMyE5bDVS", c_char),
                ("clMyParameters_ucMyReserved1", c_char),
                ("clMyParameters_ucMyReserved2", c_char),
                ("clMyParameters_ucMyE1bHealth", c_char),
                ("clMyParameters_ucMyE1bDVS", c_char),
                ("clMyParameters_ucMyReserved3", c_char),
                ("clMyParameters_ucMyReserved4", c_char),
                ("clMyParameters_usMyIODnav", c_ushort),
                ("clMyParameters_ucMySISA", c_char),
                ("clMyParameters_ucMyINAVSignalType", c_char),
                ("clMyParameters_ulMyTOE", c_uint),
                ("clMyParameters_ulMyTOC", c_ulong),
                ("clMyParameters_dMyM0", c_double),
                ("clMyParameters_dMyDeltaN", c_double),
                ("clMyParameters_dMyEcc", c_double),
                ("clMyParameters_dMyRootA", c_double),
                ("clMyParameters_dMyI0", c_double),
                ("clMyParameters_dMyIDot", c_double),
                ("clMyParameters_dMyOmega0", c_double),
                ("clMyParameters_dMyOmega", c_double),
                ("clMyParameters_dMyOmegaDot", c_double),
                ("clMyParameters_dMyCuc", c_double),
                ("clMyParameters_dMyCus", c_double),
                ("clMyParameters_dMyCrc", c_double),
                ("clMyParameters_dMyCrs", c_double),
                ("clMyParameters_dMyCic", c_double),
                ("clMyParameters_dMyCis", c_double),
                ("clMyParameters_dMyAf0", c_double),
                ("clMyParameters_dMyAf1", c_double),
                ("clMyParameters_dMyAf2", c_double),
                ("clMyParameters_dMyE1E5aBGD", c_double),
                ("clMyParameters_dMyE1E5bBGD", c_double),
                ]


# noinspection PyTypeChecker
class GALFNAVEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyParameters_ulMySatId", c_ulong),
                ("clMyParameters_ucMyE5aHealth", c_char),
                ("clMyParameters_ucMyE5aDVS", c_char),
                ("clMyParameters_ucMyReserved1", c_char),
                ("clMyParameters_ucMyReserved2", c_char),
                ("clMyParameters_usMyIODnav", c_ushort),
                ("clMyParameters_ucMySISA", c_char),
                ("clMyParameters_ucMyReserved3", c_char),
                ("clMyParameters_ulMyTOE", c_uint),
                ("clMyParameters_ulMyTOC", c_ulong),
                ("clMyParameters_dMyM0", c_double),
                ("clMyParameters_dMyDeltaN", c_double),
                ("clMyParameters_dMyEcc", c_double),
                ("clMyParameters_dMyRootA", c_double),
                ("clMyParameters_dMyI0", c_double),
                ("clMyParameters_dMyIDot", c_double),
                ("clMyParameters_dMyOmega0", c_double),
                ("clMyParameters_dMyOmega", c_double),
                ("clMyParameters_dMyOmegaDot", c_double),
                ("clMyParameters_dMyCuc", c_double),
                ("clMyParameters_dMyCus", c_double),
                ("clMyParameters_dMyCrc", c_double),
                ("clMyParameters_dMyCrs", c_double),
                ("clMyParameters_dMyCic", c_double),
                ("clMyParameters_dMyCis", c_double),
                ("clMyParameters_dMyAf0", c_double),
                ("clMyParameters_dMyAf1", c_double),
                ("clMyParameters_dMyAf2", c_double),
                ("clMyParameters_dMyE1E5aBGD", c_double),
                ]


# noinspection PyTypeChecker
class ALIGNBSLNXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyECEFBaseline_dMyX", c_double),
                ("clMyECEFBaseline_dMyY", c_double),
                ("clMyECEFBaseline_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("acMyRoverID", c_char*4),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class ALIGNBSLNENU(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySolutionStatus", c_uint),
                ("eMySolutionType", c_uint),
                ("clMyLLHBslnWRTBase_dMyLongitude", c_double),
                ("clMyLLHBslnWRTBase_dMyLatitude", c_double),
                ("clMyLLHBslnWRTBase_dMyHeight", c_double),
                ("clMyLLHStdWRTBase_fMyLongStdDev", c_float),
                ("clMyLLHStdWRTBase_fMyLatStdDev", c_float),
                ("clMyLLHStdWRTBase_fMyHgtStdDev", c_float),
                ("acMyRoverID", c_char*4),
                ("acMyMasterID", c_char*4),
                ("clMySatelliteInfo_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_ucMyNumInSolutionDualFreq", c_char),
                ("ucMyMeasurementSource", c_char),
                ("ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class HEADINGSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class HEADINGSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", HEADINGSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class VARIABLELEVERARM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("adMyOffsets", c_double*3),
                ("adMyStdevs", c_double*3),
                ]


# noinspection PyTypeChecker
class GIMBALLEDPVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class REFSTATIONINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyLatitude", c_double),
                ("dMyLongitude", c_double),
                ("dMyHeight", c_double),
                ("eMyDatum", c_uint),
                ("fMyARPHeight", c_float),
                ("ulMyHealth", c_ulong),
                ("eMyRefType", c_uint),
                ("acMyStationID", c_char*5),
                ("acMyAntennaModel", c_char*32),
                ("acMyAntennaSerial", c_char*32),
                ]


# noinspection PyTypeChecker
class TAGGEDMARK3PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyPVASolution_ulMyTagID", c_ulong),
                ]


# noinspection PyTypeChecker
class TAGGEDMARK4PVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyPVASolution_ulMyTagID", c_ulong),
                ]


# noinspection PyTypeChecker
class MODELFEATURES_aclFeatures(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eFeatureStatus", c_uint),
                ("eFeature", c_uint),
                ]


# noinspection PyTypeChecker
class MODELFEATURES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclFeatures_arraylength", c_ulong),
                ("aclFeatures", MODELFEATURES_aclFeatures*30),
                ]


# noinspection PyTypeChecker
class QZSSRAWSUBFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("clMyRawSubframeData_ulMySubFrameID", c_ulong),
                ("clMyRawSubframeData_aucMyRawSubFrameData", c_char*30),
                ("ulMySignalChannelNumber", c_ulong),
                ]


# noinspection PyTypeChecker
class QZSSRAWEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyWeek", c_ulong),
                ("ulMyTOE", c_ulong),
                ("clMyRawEphemerisData_aucMySubframe1", c_char*30),
                ("clMyRawEphemerisData_aucMySubframe2", c_char*30),
                ("clMyRawEphemerisData_aucMySubframe3", c_char*30),
                ]


# noinspection PyTypeChecker
class ALIGNDOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDop_fMyGDOP", c_float),
                ("clMyDop_fMyPDOP", c_float),
                ("clMyDop_fMyHDOP", c_float),
                ("clMyDop_fMyHTDOP", c_float),
                ("clMyDop_fMyTDOP", c_float),
                ("clMyDop_fMyGPSElevMask", c_float),
                ("clMyDop_aulMySats_Len", c_ulong),
                ("clMyDop_aulMySats", c_ulong*325),
                ]


# noinspection PyTypeChecker
class HEADING2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("fFloat", c_float),
                ("clMyHeadingInfo_fMyHeadingStdDev", c_float),
                ("clMyHeadingInfo_fMyPitchStdDev", c_float),
                ("acMyRoverID", c_char*4),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class QZSSEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyEphemerisData_ulMySatelliteID", c_ulong),
                ("clMyEphemerisData_dMyTOW", c_double),
                ("clMyEphemerisData_ulMyHealth6", c_ulong),
                ("clMyEphemerisData_ulMyIODE1", c_ulong),
                ("clMyEphemerisData_ulMyIODE2", c_ulong),
                ("clMyEphemerisData_ulMyWN", c_ulong),
                ("clMyEphemerisData_ulMyZWN", c_ulong),
                ("clMyEphemerisData_dMyTOE", c_double),
                ("clMyEphemerisData_dMyA", c_double),
                ("clMyEphemerisData_dMyDeltaN", c_double),
                ("clMyEphemerisData_dMyM0", c_double),
                ("clMyEphemerisData_dMyEcc", c_double),
                ("clMyEphemerisData_dMyOmega", c_double),
                ("clMyEphemerisData_dMyCuc", c_double),
                ("clMyEphemerisData_dMyCus", c_double),
                ("clMyEphemerisData_dMyCrc", c_double),
                ("clMyEphemerisData_dMyCrs", c_double),
                ("clMyEphemerisData_dMyCic", c_double),
                ("clMyEphemerisData_dMyCis", c_double),
                ("clMyEphemerisData_dMyI0", c_double),
                ("clMyEphemerisData_dMyIDot", c_double),
                ("clMyEphemerisData_dMyOmega0", c_double),
                ("clMyEphemerisData_dMyOmegaDot", c_double),
                ("clMyEphemerisData_ulMyIODC", c_ulong),
                ("clMyEphemerisData_dMyTOC", c_double),
                ("clMyEphemerisData_dMyTGD", c_double),
                ("clMyEphemerisData_dMyAf0", c_double),
                ("clMyEphemerisData_dMyAf1", c_double),
                ("clMyEphemerisData_dMyAf2", c_double),
                ("clMyEphemerisData_bMyAntiSpoofing", c_bool),
                ("clMyEphemerisData_dMyN", c_double),
                ("clMyEphemerisData_dMyEphVar", c_double),
                ("clMyEphemerisData_ucMyFitInterval", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ]


# noinspection PyTypeChecker
class RTCAOBS3_clMyData_Transmitter2Data(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("FreqAvail", c_char),
                ("L1ADROffset", c_double),
                ("L1PsrOffset", c_double),
                ("CodeType", c_char),
                ("L1LockTime", c_char),
                ("Reserved", c_char),
                ("L2ADROffset", c_double),
                ("L2PsrOffset", c_double),
                ("CodeType2", c_char),
                ("L2LockTime", c_char),
                ("Reserved2", c_char),
                ]


# noinspection PyTypeChecker
class RTCAOBS3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyData_NovAtelDesignator", c_char),
                ("clMyData_SubtypeIndicator", c_char),
                ("clMyData_bMyMovingBase", c_bool),
                ("clMyData_dMyRefX", c_double),
                ("clMyData_dMyRefY", c_double),
                ("clMyData_dMyRefZ", c_double),
                ("clMyData_Seconds", c_float),
                ("clMyData_ReceiverTimeBias", c_double),
                ("clMyData_Reserved", c_int),
                ("clMyData_Transmitter2Data_arraylength", c_ulong),
                ("clMyData_Transmitter2Data", RTCAOBS3_clMyData_Transmitter2Data*72),
                ]


# noinspection PyTypeChecker
class RTCAOBS3IN_clMyRTCAOBS_Transmitter2Data(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("TransmitterID", c_char),
                ("FreqAvail", c_char),
                ("L1ADROffset", c_double),
                ("L1PsrOffset", c_double),
                ("CodeType", c_char),
                ("L1LockTime", c_char),
                ("Reserved", c_char),
                ("L2ADROffset", c_double),
                ("L2PsrOffset", c_double),
                ("CodeType2", c_char),
                ("L2LockTime", c_char),
                ("Reserved2", c_char),
                ]


# noinspection PyTypeChecker
class RTCAOBS3IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clHeader_clMyRTCAOBS_ulMessageIdentifier", c_ulong),
                ("clHeader_clMyRTCAOBS_ulRefStation", c_ulong),
                ("clHeader_clMyRTCAOBS_ulMessageType", c_ulong),
                ("clHeader_clMyRTCAOBS_ulReserved", c_ulong),
                ("clHeader_clMyRTCAOBS_ulMessageLength", c_ulong),
                ("clMyRTCAOBS_NovAtelDesignator", c_char),
                ("clMyRTCAOBS_SubtypeIndicator", c_char),
                ("clMyRTCAOBS_bMyMovingBase", c_bool),
                ("clMyRTCAOBS_dMyRefX", c_double),
                ("clMyRTCAOBS_dMyRefY", c_double),
                ("clMyRTCAOBS_dMyRefZ", c_double),
                ("clMyRTCAOBS_Seconds", c_float),
                ("clMyRTCAOBS_ReceiverTimeBias", c_double),
                ("clMyRTCAOBS_Reserved", c_int),
                ("clMyRTCAOBS_Transmitter2Data_arraylength", c_ulong),
                ("clMyRTCAOBS_Transmitter2Data", RTCAOBS3IN_clMyRTCAOBS_Transmitter2Data*72),
                ]


# noinspection PyTypeChecker
class SOURCETABLE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySourceTableEntry_sMyEndpoint", c_char*80),
                ("clMySourceTableEntry_ulMyReserved1", c_ulong),
                ("clMySourceTableEntry_ulMyReserved2", c_ulong),
                ("clMySourceTableEntry_sMyEntryData", c_char*512),
                ]


# noinspection PyTypeChecker
class QZSSRAWALMANAC_aclMySubFramePages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usSVID", c_ushort),
                ("aucMyPageRawData", c_char*30),
                ]


# noinspection PyTypeChecker
class QZSSRAWALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyTOA_ulMyWeeks", c_ulong),
                ("clMyTOA_ulMyMilliseconds", c_ulong),
                ("aclMySubFramePages_arraylength", c_ulong),
                ("aclMySubFramePages", QZSSRAWALMANAC_aclMySubFramePages*46),
                ]


# noinspection PyTypeChecker
class QZSSALMANAC_aclMySVAlmData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulPRN", c_ulong),
                ("ulMyWn", c_ulong),
                ("dMyTOA", c_double),
                ("dMyEcc", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmega", c_double),
                ("dMyMo", c_double),
                ("dMyAf0", c_double),
                ("dMyAf1", c_double),
                ("dMyN", c_double),
                ("dMyA", c_double),
                ("dMyDi", c_double),
                ("ulMyHealth6", c_ulong),
                ("ulMyHealth8", c_ulong),
                ]


# noinspection PyTypeChecker
class QZSSALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySVAlmData_arraylength", c_ulong),
                ("aclMySVAlmData", QZSSALMANAC_aclMySVAlmData*139),
                ]


# noinspection PyTypeChecker
class QZSSIONUTC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyIon_dMyA0", c_double),
                ("clMyIon_dMyA1", c_double),
                ("clMyIon_dMyA2", c_double),
                ("clMyIon_dMyA3", c_double),
                ("clMyIon_dMyB0", c_double),
                ("clMyIon_dMyB1", c_double),
                ("clMyIon_dMyB2", c_double),
                ("clMyIon_dMyB3", c_double),
                ("clMyUTC_ulMyWNt", c_ulong),
                ("clMyUTC_ulMyTot", c_ulong),
                ("clMyUTC_dMyA0", c_double),
                ("clMyUTC_dMyA1", c_double),
                ("clMyUTC_ulMyWNlsf", c_ulong),
                ("clMyUTC_ulMyDN", c_ulong),
                ("clMyUTC_lMyDeltaTls", c_long),
                ("clMyUTC_lMyDeltaTlsf", c_long),
                ("clMyUTC_ulMyDeltaTUTC", c_ulong),
                ]


# noinspection PyTypeChecker
class AUTHCODES_clMyAuthCodes(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyType", c_uint),
                ("bMyValid", c_bool),
                ("aszMyAuthCode", c_char*80),
                ]


# noinspection PyTypeChecker
class AUTHCODES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eSignatureStatus", c_uint),
                ("clMyAuthCodes_arraylength", c_ulong),
                ("clMyAuthCodes", AUTHCODES_clMyAuthCodes*24),
                ]


# noinspection PyTypeChecker
class GENERATEALIGNCORRECTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("ulMyBaudRate", c_ulong),
                ("ulMyObsRateInHz", c_ulong),
                ("ulMyRefRateInHz", c_ulong),
                ("eMyCorrectionInterface", c_uint),
                ]


# noinspection PyTypeChecker
class SBASHANDLERSSTATUS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("eMyServiceProvider", c_uint),
                ("bMyIsTestMode", c_bool),
                ("ulMyIODP", c_ulong),
                ("ulMyIODI", c_ulong),
                ("fMyElevationInDegrees", c_float),
                ("fMyLockTime", c_float),
                ("clMyLastFastMessageTime_ulMyMilliseconds", c_ulong),
                ("clMyLastGoodMessageTime_ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class SBASHANDLERSSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyActiveHandlerPRN", c_ulong),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", SBASHANDLERSSTATUS_aclMyEntries*8),
                ]


# noinspection PyTypeChecker
class SBASHANDLEREVENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("eMyType", c_uint),
                ]


# noinspection PyTypeChecker
class IMURATECORRIMUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyAttitudeRate_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitudeRate_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitudeRate_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyVehicleAccel_clMyPVASolution_dMyLateral", c_double),
                ("clMyVehicleAccel_clMyPVASolution_dMyLongitudinal", c_double),
                ("clMyVehicleAccel_clMyPVASolution_dMyVertical", c_double),
                ]


# noinspection PyTypeChecker
class RTCM4093TYPE0(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM4093IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class RTCM4093TYPE1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM4093TYPE2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM4093TYPE3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM4093TYPE4(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class INSUPDATEDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPosType", c_uint),
                ("iMyGNSSPosRejectCode", c_int),
                ]


# noinspection PyTypeChecker
class RTKATMOSPHEREDELAYS_aclMyAtmosphereDelays(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyL1Iono", c_float),
                ("fMyTropo", c_float),
                ]


# noinspection PyTypeChecker
class RTKATMOSPHEREDELAYS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyAtmosphereDelays_arraylength", c_ulong),
                ("aclMyAtmosphereDelays", RTKATMOSPHEREDELAYS_aclMyAtmosphereDelays*74),
                ]


# noinspection PyTypeChecker
class RTKAMBIGUITIES_aclMyAmbiguities(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyFrequency", c_uint),
                ("eMyAmbiguityStatus", c_uint),
                ("fMyAmbiguity", c_float),
                ("fMyAmbiguityStdDev", c_float),
                ("fMyResidual", c_float),
                ]


# noinspection PyTypeChecker
class RTKAMBIGUITIES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyAmbiguities_arraylength", c_ulong),
                ("aclMyAmbiguities", RTKAMBIGUITIES_aclMyAmbiguities*229),
                ]


# noinspection PyTypeChecker
class MOTION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMotion", c_uint),
                ("dMySpeed", c_double),
                ]


# noinspection PyTypeChecker
class HEAVE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeaveInfo_ulMyWeek", c_ulong),
                ("clMyHeaveInfo_dMySeconds", c_double),
                ("clMyHeaveInfo_dMyHeave", c_double),
                ]


# noinspection PyTypeChecker
class ISMRAWOBS_aclMyRawObservationEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySVID", c_char),
                ("cMyFrequency", c_char),
                ("ucMySignalType", c_char),
                ("ucMyReserved1", c_char),
                ("dMyFirstADR", c_double),
                ("ulMyFirstPower", c_ulong),
                ("aulMyScintObservations", c_ulong*49),
                ]


# noinspection PyTypeChecker
class ISMRAWOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("aclMyRawObservationEntries_arraylength", c_ulong),
                ("aclMyRawObservationEntries", ISMRAWOBS_aclMyRawObservationEntries*56),
                ]


# noinspection PyTypeChecker
class ISMRAWTEC_aclMyRawTECEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySVID", c_char),
                ("cMyFrequency", c_char),
                ("ucMySatelliteSystem", c_char),
                ("ucMyPrimarySignal", c_char),
                ("ucMySecondarySignal", c_char),
                ("ucMyReserved1", c_char),
                ("ucMyReserved2", c_char),
                ("ucMyReserved3", c_char),
                ("fMyTEC", c_float),
                ("fMyDeltaTEC", c_float),
                ]


# noinspection PyTypeChecker
class ISMRAWTEC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyRawTECEntries_arraylength", c_ulong),
                ("aclMyRawTECEntries", ISMRAWTEC_aclMyRawTECEntries*325),
                ]


# noinspection PyTypeChecker
class ISMREDOBS_aclMyReducedObsEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySVID", c_char),
                ("cMyFrequency", c_char),
                ("ucMySatelliteSystem", c_char),
                ("ucMySignalType", c_char),
                ("fMyAzimuth", c_float),
                ("fMyElevation", c_float),
                ("fMyCNo", c_float),
                ("fMyLockTime", c_float),
                ("fMyCMCAverage", c_float),
                ("fMyCMCStdDev", c_float),
                ("fMyS4", c_float),
                ("fMyS4Correction", c_float),
                ("fMyPhase1SecStdDev", c_float),
                ("fMyPhase3SecStdDev", c_float),
                ("fMyPhase10SecStdDev", c_float),
                ("fMyPhase30SecStdDev", c_float),
                ("fMyPhase60SecStdDev", c_float),
                ]


# noinspection PyTypeChecker
class ISMREDOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyReducedObsEntries_arraylength", c_ulong),
                ("aclMyReducedObsEntries", ISMREDOBS_aclMyReducedObsEntries*325),
                ]


# noinspection PyTypeChecker
class ISMREDTEC_aclMyReducedTECEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySVID", c_char),
                ("cMyFrequency", c_char),
                ("ucMySatelliteSystem", c_char),
                ("ucMyPrimarySignal", c_char),
                ("ucMySecondarySignal", c_char),
                ("ucMyReserved1", c_char),
                ("ucMyReserved2", c_char),
                ("ucMyReserved3", c_char),
                ("fMyAzimuth", c_float),
                ("fMyElevation", c_float),
                ("fMySecondaryLockTime", c_float),
                ("fMySecondaryCNo", c_float),
                ("fMyTEC15", c_float),
                ("fMyDeltaTEC15", c_float),
                ("fMyTEC30", c_float),
                ("fMyDeltaTEC30", c_float),
                ("fMyTEC45", c_float),
                ("fMyDeltaTEC45", c_float),
                ("fMyTECTOW", c_float),
                ("fMyDeltaTECTOW", c_float),
                ]


# noinspection PyTypeChecker
class ISMREDTEC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyReducedTECEntries_arraylength", c_ulong),
                ("aclMyReducedTECEntries", ISMREDTEC_aclMyReducedTECEntries*325),
                ]


# noinspection PyTypeChecker
class ISMDETOBS_aclMyDetrendedEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySVID", c_char),
                ("cMyFrequency", c_char),
                ("ucMySignalType", c_char),
                ("ucMyReserved1", c_char),
                ("dMyFirstADR", c_double),
                ("ulMyFirstPower", c_ulong),
                ("aulMyScintObservations", c_ulong*49),
                ]


# noinspection PyTypeChecker
class ISMDETOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("aclMyDetrendedEntries_arraylength", c_ulong),
                ("aclMyDetrendedEntries", ISMDETOBS_aclMyDetrendedEntries*56),
                ]


# noinspection PyTypeChecker
class EXTERNALPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyLatitude", c_double),
                ("dMyLongitude", c_double),
                ("dMyHeight", c_double),
                ("dMyLatitudeStdDev", c_double),
                ("dMyLongitudeStdDev", c_double),
                ("dMyHeightStdDev", c_double),
                ("ulMyUpdateType", c_ulong),
                ]


# noinspection PyTypeChecker
class DECODEDBASESTATIONOBS_clMyObservationsBase_aclMyObs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySvPrn", c_ushort),
                ("usMySvFreq", c_ushort),
                ("dMyPsr", c_double),
                ("fMySDPsr", c_float),
                ("dMyAdr", c_double),
                ("fMySDAdr", c_float),
                ("fMyDop", c_float),
                ("fMyUserCNo", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class DECODEDBASESTATIONOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyObservationsBase_aclMyObs_arraylength", c_ulong),
                ("clMyObservationsBase_aclMyObs", DECODEDBASESTATIONOBS_clMyObservationsBase_aclMyObs*325),
                ]


# noinspection PyTypeChecker
class ISMCALIBRATIONSTATUS_aclMyCalibrationStatuses(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignalCombination", c_uint),
                ("ulMyNumSamples", c_ulong),
                ("fMyTECCalibration", c_float),
                ("fMyTECStdDev", c_float),
                ]


# noinspection PyTypeChecker
class ISMCALIBRATIONSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyCalibrationTimeSec", c_ulong),
                ("aclMyCalibrationStatuses_arraylength", c_ulong),
                ("aclMyCalibrationStatuses", ISMCALIBRATIONSTATUS_aclMyCalibrationStatuses*12),
                ]


# noinspection PyTypeChecker
class PROFILEINFO_aclMyProfileInfoCommand(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sMyCommand", c_char*201),
                ]


# noinspection PyTypeChecker
class PROFILEINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sMyProfileName", c_char*20),
                ("ulMyStatus", c_ulong),
                ("aclMyProfileInfoCommand_arraylength", c_ulong),
                ("aclMyProfileInfoCommand", PROFILEINFO_aclMyProfileInfoCommand*20),
                ]


# noinspection PyTypeChecker
class GALFNAVRAWPAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMySatId", c_ulong),
                ("aucMyRawFrameData", c_char*27),
                ]


# noinspection PyTypeChecker
class GALINAVRAWWORD(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMySatId", c_ulong),
                ("eMySignalType", c_uint),
                ("aucMyRawFrameData", c_char*16),
                ]


# noinspection PyTypeChecker
class THISANTENNAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyStationID", c_char*4),
                ("szMyModelName", c_char*32),
                ("szMySerialNumber", c_char*32),
                ("ulMySetupID", c_ulong),
                ]


# noinspection PyTypeChecker
class BASEANTENNAPCCORRECTION_aclMyPhaseCenterVariationCorrection(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatID_idMyID", satelliteid),
                ("clMySatID_eMySystemType", c_uint),
                ("eFrequency", c_uint),
                ("dPSRCorrection", c_double),
                ("dADRCorrection", c_double),
                ]


# noinspection PyTypeChecker
class BASEANTENNAPCCORRECTION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyDiffStationID", c_char*4),
                ("eMyCorrType ", c_uint),
                ("adMyPhaseCenterXYZOffSet", c_double*3),
                ("adMyPhaseCenterENUOffset", c_double*3),
                ("aclMyPhaseCenterVariationCorrection_arraylength", c_ulong),
                ("aclMyPhaseCenterVariationCorrection", BASEANTENNAPCCORRECTION_aclMyPhaseCenterVariationCorrection*325),
                ]


# noinspection PyTypeChecker
class THISANTENNAPCCORRECTION_aclMyPhaseCenterVariationCorrection(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatID_idMyID", satelliteid),
                ("clMySatID_eMySystemType", c_uint),
                ("eFrequency", c_uint),
                ("dPSRCorrection", c_double),
                ("dADRCorrection", c_double),
                ]


# noinspection PyTypeChecker
class THISANTENNAPCCORRECTION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyDiffStationID", c_char*4),
                ("eMyCorrType ", c_uint),
                ("adMyPhaseCenterXYZOffSet", c_double*3),
                ("adMyPhaseCenterENUOffset", c_double*3),
                ("aclMyPhaseCenterVariationCorrection_arraylength", c_ulong),
                ("aclMyPhaseCenterVariationCorrection", THISANTENNAPCCORRECTION_aclMyPhaseCenterVariationCorrection*325),
                ]


# noinspection PyTypeChecker
class SBASALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("eMySystemVariant", c_uint),
                ("ulMyt0", c_ulong),
                ("usMyDataID", c_ushort),
                ("usMyHealth", c_ushort),
                ("lMyX", c_long),
                ("lMyY", c_long),
                ("lMyZ", c_long),
                ("lMyXVel", c_long),
                ("lMyYVel", c_long),
                ("lMyZVel", c_long),
                ]


# noinspection PyTypeChecker
class CORRECTIONSTATS_aclMyCorrectionMessage(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("ulMyUnknownBytes", c_ulong),
                ("eMyType", c_uint),
                ("ulMyInvalidCount", c_ulong),
                ("acMyID", c_char*4),
                ("ulMyType", c_ulong),
                ("ulMySubType", c_ulong),
                ("clMyLastTime_ulMyMilliseconds", c_ulong),
                ("ulMyCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CORRECTIONSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyCorrectionMessage_arraylength", c_ulong),
                ("aclMyCorrectionMessage", CORRECTIONSTATS_aclMyCorrectionMessage*50),
                ]


# noinspection PyTypeChecker
class BESTGNSSPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class BESTGNSSVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("fFloat", c_float),
                ]


# noinspection PyTypeChecker
class RAWIMUCOMDATAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyIMUIFType", c_uint),
                ("eMyPort", c_uint),
                ("ucMyMsgID", c_char),
                ("ucMyPacketCount", c_char),
                ("ucMyReserved1", c_char),
                ("ucMyReserved2", c_char),
                ("aucMyRawData_Len", c_ulong),
                ("aucMyRawData", c_char*128),
                ]


# noinspection PyTypeChecker
class SYNCTIMETRIGGER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class RELINSPVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRelINSPVAInfo_eMyRelINSOutput", c_uint),
                ("clMyRelINSPVAInfo_dMyDeltaPosN", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPosE", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPosU", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelN", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelE", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelU", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaRoll", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPitch", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaHeading", c_double),
                ("clMyRelINSPVAInfo_fMyDifferentialLag", c_float),
                ("clMyRelINSPVAInfo_acMyRoverID", c_char*4),
                ("clMyRelINSPVAInfo_eMyRoverINSStatus", c_uint),
                ("clMyRelINSPVAInfo_acMyMasterID", c_char*4),
                ("clMyRelINSPVAInfo_eMyMasterINSStatus", c_uint),
                ("clMyRelINSPVAInfo_eMyRTKBaselineStatus", c_uint),
                ("clMyRelINSPVAInfo_ulMyExtendedSolStat", c_ulong),
                ]


# noinspection PyTypeChecker
class SATXYZ2_aclMySats(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("clMyXYZRB_dMyX", c_double),
                ("clMyXYZRB_dMyY", c_double),
                ("clMyXYZRB_dMyZ", c_double),
                ("clMyXYZRB_dMyRB", c_double),
                ("dMyIonoCorr", c_double),
                ("dMyTropoCorr", c_double),
                ("dMyDummy", c_double),
                ("dMyDummy", c_double),
                ]


# noinspection PyTypeChecker
class SATXYZ2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySats_arraylength", c_ulong),
                ("aclMySats", SATXYZ2_aclMySats*72),
                ]


# noinspection PyTypeChecker
class RTKNETWORKGEOMETRICDELAYS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ("dMyGeometricDelay", c_double),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class RTKNETWORKGEOMETRICDELAYS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyNetworkType", c_uint),
                ("acMyBaseID", c_char*4),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", RTKNETWORKGEOMETRICDELAYS_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class RTKNETWORKIONOSPHERICDELAYS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("clMyTime_ulMyMilliseconds", c_ulong),
                ("dMyIonosphericDelay", c_double),
                ]


# noinspection PyTypeChecker
class RTKNETWORKIONOSPHERICDELAYS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyNetworkType", c_uint),
                ("acMyBaseID", c_char*4),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", RTKNETWORKIONOSPHERICDELAYS_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class MACNETWORK_aclMyStations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStationID", c_ulong),
                ("dMyLatitudeInDegrees", c_double),
                ("dMyLongitudeInDegrees", c_double),
                ("dMyHeight", c_double),
                ]


# noinspection PyTypeChecker
class MACNETWORK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNetworkID", c_ulong),
                ("ulMySubnetworkID", c_ulong),
                ("ulMyMasterReferenceID", c_ulong),
                ("aclMyStations_arraylength", c_ulong),
                ("aclMyStations", MACNETWORK_aclMyStations*32),
                ]


# noinspection PyTypeChecker
class TSS1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyHeaveInfo_dMyHeave", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ]


# noinspection PyTypeChecker
class INSATTX(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyCommonSolution_clMyPVASolution_eMyPositionType", c_uint),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyRollStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyPitchStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyAzimuthStdDev", c_float),
                ("clMyPVASolution_ulMyExtendedSolStat", c_ulong),
                ("clMyPVASolution_usMyTimeSincePosUpt", c_ushort),
                ]


# noinspection PyTypeChecker
class INSVELX(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyCommonSolution_clMyPVASolution_eMyPositionType", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyZStdDev", c_float),
                ("clMyPVASolution_ulMyExtendedSolStat", c_ulong),
                ("clMyPVASolution_usMyTimeSincePosUpt", c_ushort),
                ]


# noinspection PyTypeChecker
class INSPOSX(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyCommonSolution_clMyPVASolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyUndulation", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyHgtStdDev", c_float),
                ("clMyPVASolution_ulMyExtendedSolStat", c_ulong),
                ("clMyPVASolution_usMyTimeSincePosUpt", c_ushort),
                ]


# noinspection PyTypeChecker
class RAWIMUX(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRawIMUData_ucMyIMUStatusInfo", c_char),
                ("clMyRawIMUData_ucMyIMUType", c_char),
                ("clMyRawIMUData_usMyGPSWeek", c_ushort),
                ("clMyRawIMUData_dMyGPSSeconds", c_double),
                ("clMyRawIMUData_ulMyIMUStatus", c_ulong),
                ("clMyRawIMUData_alMyExternalIMUObs", c_long*6),
                ]


# noinspection PyTypeChecker
class RAWIMUSX(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRawIMUData_ucMyIMUStatusInfo", c_char),
                ("clMyRawIMUData_ucMyIMUType", c_char),
                ("clMyRawIMUData_usMyGPSWeek", c_ushort),
                ("clMyRawIMUData_dMyGPSSeconds", c_double),
                ("clMyRawIMUData_ulMyIMUStatus", c_ulong),
                ("clMyRawIMUData_alMyExternalIMUObs", c_long*6),
                ]


# noinspection PyTypeChecker
class EXTERNALPVAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyPosition1", c_double),
                ("dMyPosition2", c_double),
                ("dMyPosition3", c_double),
                ("fMyVelocity1", c_float),
                ("fMyVelocity2", c_float),
                ("fMyVelocity3", c_float),
                ("fMyAttitude1", c_float),
                ("fMyAttitude2", c_float),
                ("fMyAttitude3", c_float),
                ("fMyPositionStdDev1", c_float),
                ("fMyPositionStdDev2", c_float),
                ("fMyPositionStdDev3", c_float),
                ("fMyVelocityStdDev1", c_float),
                ("fMyVelocityStdDev2", c_float),
                ("fMyVelocityStdDev3", c_float),
                ("fMyAttitudeStdDev1", c_float),
                ("fMyAttitudeStdDev2", c_float),
                ("fMyAttitudeStdDev3", c_float),
                ("ulMyUpdateType", c_ulong),
                ("ulMyOptions", c_ulong),
                ]


# noinspection PyTypeChecker
class INSPVAX(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyCommonSolution_clMyPVASolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyUndulation", c_float),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyHgtStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyZStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyRollStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyPitchStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyAzimuthStdDev", c_float),
                ("clMyPVASolution_ulMyExtendedSolStat", c_ulong),
                ("clMyPVASolution_usMyTimeSincePosUpt", c_ushort),
                ]


# noinspection PyTypeChecker
class INSLEVERARMS_aclMyLeverArm(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iMyMapping", c_int),
                ("clMyEnclosure_afMyElements", c_float*3),
                ("clMyEnclosureStdev_afMyElements", c_float*3),
                ("eMyOffset", c_uint),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSLEVERARMS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyLeverArm_arraylength", c_ulong),
                ("aclMyLeverArm", INSLEVERARMS_aclMyLeverArm*3),
                ]


# noinspection PyTypeChecker
class INSOFFSETS_aclMyLeverArm(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOffset", c_uint),
                ("clMyEnclosure_afMyElements", c_float*3),
                ("clMyEnclosureStdev_afMyElements", c_float*3),
                ("eMyInputFrame", c_uint),
                ("eMyStatus", c_uint),
                ("ulExtendedStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class INSOFFSETS_aclMySolutionTranslation(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOffset", c_uint),
                ("clMyEnclosure_afMyElements", c_float*3),
                ("clMyEnclosureStdev_afMyElements", c_float*3),
                ("eMyInputFrame", c_uint),
                ("eMyStatus", c_uint),
                ("ulExtendedStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class INSOFFSETS_aclMyEulerSolutionRotation(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOffset", c_uint),
                ("clMyEnclosure_afMyElements", c_float*3),
                ("clMyEnclosureStdev_afMyElements", c_float*3),
                ("eMyInputFrame", c_uint),
                ("eMyStatus", c_uint),
                ("ulExtendedStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class INSOFFSETS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iMyMapping", c_int),
                ("iMyGimbalMapping", c_int),
                ("bMyApplyRbvRotation", c_bool),
                ("bMyHaveDualAntenna", c_bool),
                ("bMyIsGimballed", c_bool),
                ("aclMyLeverArm_arraylength", c_ulong),
                ("aclMyLeverArm", INSOFFSETS_aclMyLeverArm*3),
                ("aclMySolutionTranslation_arraylength", c_ulong),
                ("aclMySolutionTranslation", INSOFFSETS_aclMySolutionTranslation*7),
                ("aclMyEulerSolutionRotation_arraylength", c_ulong),
                ("aclMyEulerSolutionRotation", INSOFFSETS_aclMyEulerSolutionRotation*9),
                ]


# noinspection PyTypeChecker
class INSVARIABLELEVERARMS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("adMyOffsets", c_double*3),
                ("adMyStdevs", c_double*3),
                ]


# noinspection PyTypeChecker
class RTCM1071(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1072(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1073(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1074(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1075(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1076(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1077(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1081(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1082(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1083(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1084(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1085(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1086(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1087(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1091(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1092(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1093(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1094(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1095(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1096(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1097(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class MATCHEDRESET(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyCause", c_char*256),
                ]


# noinspection PyTypeChecker
class RTKGLOBIAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyEngine", c_char*2),
                ("eMyReceiverType", c_uint),
                ("eMyBiasType", c_uint),
                ("dMyBias", c_double),
                ("dMyMeanBias", c_double),
                ("dMySampleSTD", c_double),
                ("ulMySampleCount", c_ulong),
                ]


# noinspection PyTypeChecker
class LEDSTATES_aclMyLedStates(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyLedID", c_uint),
                ("eMyLedPatternState", c_uint),
                ]


# noinspection PyTypeChecker
class LEDSTATES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyLedStates_arraylength", c_ulong),
                ("aclMyLedStates", LEDSTATES_aclMyLedStates*15),
                ]


# noinspection PyTypeChecker
class GPSCNAVEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCNAVEphemerisData_ulMySatelliteID", c_ulong),
                ("clMyCNAVEphemerisData_dMyTOW", c_double),
                ("clMyCNAVEphemerisData_bMyAlert", c_bool),
                ("clMyCNAVEphemerisData_ulMyWNe", c_ulong),
                ("clMyCNAVEphemerisData_ulMyHealth", c_ulong),
                ("clMyCNAVEphemerisData_dMyTOp", c_double),
                ("clMyCNAVEphemerisData_lMyURAedIndex", c_long),
                ("clMyCNAVEphemerisData_dMyTOe", c_double),
                ("clMyCNAVEphemerisData_dMyDeltaA", c_double),
                ("clMyCNAVEphemerisData_dMyAdot", c_double),
                ("clMyCNAVEphemerisData_dMyDeltaN", c_double),
                ("clMyCNAVEphemerisData_dMyDeltaNDot", c_double),
                ("clMyCNAVEphemerisData_dMyM0", c_double),
                ("clMyCNAVEphemerisData_dMyEcc", c_double),
                ("clMyCNAVEphemerisData_dMyOmega", c_double),
                ("clMyCNAVEphemerisData_ucMyISFlag", c_char),
                ("clMyCNAVEphemerisData_ucMyL2CPhasing", c_char),
                ("clMyCNAVEphemerisData_ucMySource", c_char),
                ("clMyCNAVEphemerisData_ucReserved", c_char),
                ("clMyCNAVEphemerisData_dMyOmega0", c_double),
                ("clMyCNAVEphemerisData_dMyI0", c_double),
                ("clMyCNAVEphemerisData_dMyDOD", c_double),
                ("clMyCNAVEphemerisData_dMyIDot", c_double),
                ("clMyCNAVEphemerisData_dMyCis", c_double),
                ("clMyCNAVEphemerisData_dMyCic", c_double),
                ("clMyCNAVEphemerisData_dMyCrs", c_double),
                ("clMyCNAVEphemerisData_dMyCrc", c_double),
                ("clMyCNAVEphemerisData_dMyCus", c_double),
                ("clMyCNAVEphemerisData_dMyCuc", c_double),
                ("clMyCNAVEphemerisData_lMyURAnedIndex", c_long),
                ("clMyCNAVEphemerisData_ulMyURAned1Index", c_double),
                ("clMyCNAVEphemerisData_ulMyURAned2Index", c_double),
                ("clMyCNAVEphemerisData_dMyTOc", c_double),
                ("clMyCNAVEphemerisData_dMyAf0", c_double),
                ("clMyCNAVEphemerisData_dMyAf1", c_double),
                ("clMyCNAVEphemerisData_dMyAf2", c_double),
                ]


# noinspection PyTypeChecker
class GPSRAWCNAVEPHEM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySignalChannelNumber", c_ulong),
                ("ulMySatelliteID", c_ulong),
                ("ulMyWNe", c_ulong),
                ("dMyTOp", c_double),
                ("dMyTOe", c_double),
                ("dMyTOc", c_double),
                ("clMyCNAVRawEphemerisData_aucMyMessage10", c_char*38),
                ("clMyCNAVRawEphemerisData_aucMyMessage11", c_char*38),
                ("clMyCNAVRawEphemerisData_aucMyMessageClock", c_char*16),
                ]


# noinspection PyTypeChecker
class GPSCNAVMIDIALM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTransmittingPRN", c_ulong),
                ("ulMyPRNa", c_ulong),
                ("ulMyWNa", c_ulong),
                ("dMyTOa", c_double),
                ("ulMyHealth", c_ulong),
                ("dMyEcc", c_double),
                ("dMyDeltaI", c_double),
                ("dMyOmegaDot", c_double),
                ("dMySqrtA", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmega", c_double),
                ("dMyM0", c_double),
                ("dMyAf0", c_double),
                ("dMyAf1", c_double),
                ]


# noinspection PyTypeChecker
class GPSRAWCNAVMIDIALM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTransmittingPRN", c_ulong),
                ("ulMyPRNa", c_ulong),
                ("ulMyWNa", c_ulong),
                ("dMyTOa", c_double),
                ("aucMyMessageMidiALM", c_char*19),
                ]


# noinspection PyTypeChecker
class GPSCNAVREDUCEDALM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTransmittingPRN", c_ulong),
                ("ulMyPRNa", c_ulong),
                ("ulMyWNa", c_ulong),
                ("dMyTOa", c_double),
                ("dMyDeltaA", c_double),
                ("dMyOmega0", c_double),
                ("dMyPhi0", c_double),
                ("ulMyHealth", c_ulong),
                ]


# noinspection PyTypeChecker
class GPSRAWCNAVREDUCEDALM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTransmittingPRN", c_ulong),
                ("ulMyPRNa", c_ulong),
                ("ulMyWNa", c_ulong),
                ("dMyTOa", c_double),
                ("aucMyMessageReducedALM", c_char*4),
                ]


# noinspection PyTypeChecker
class GPSCNAVIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyWNop", c_ulong),
                ("ulMyTop", c_ulong),
                ("dMyAlpha0", c_double),
                ("dMyAlpha1", c_double),
                ("dMyAlpha2", c_double),
                ("dMyAlpha3", c_double),
                ("dMyBeeta0", c_double),
                ("dMyBeeta1", c_double),
                ("dMyBeeta2", c_double),
                ("dMyBeeta3", c_double),
                ]


# noinspection PyTypeChecker
class GPSCNAVGROUPDELAY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyWNop", c_ulong),
                ("ulMyTop", c_ulong),
                ("dMyTgd", c_double),
                ("dMyISCl1ca", c_double),
                ("dMyISCl2c", c_double),
                ("dMyISCl5i5", c_double),
                ("dMyISCl5q5", c_double),
                ]


# noinspection PyTypeChecker
class GPSCNAVUTC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("dMyA0", c_double),
                ("dMyA1", c_double),
                ("dMyA2", c_double),
                ("lMyDeltaTls", c_long),
                ("ulMyTot", c_ulong),
                ("ulMyWNot", c_ulong),
                ("ulMyWNlsf", c_ulong),
                ("ulMyDN", c_ulong),
                ("lMyDeltaTlsf", c_long),
                ]


# noinspection PyTypeChecker
class GPSCNAVEOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyTeop", c_ulong),
                ("dMyPMx", c_double),
                ("dMyPMxdot", c_double),
                ("dMyPMy", c_double),
                ("dMyPMydot", c_double),
                ("dMyDeltaUT1", c_double),
                ("dMyDeltaUT1dot", c_double),
                ]


# noinspection PyTypeChecker
class GPSCNAVGGTO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyTggto", c_ulong),
                ("ulMyWNggto", c_ulong),
                ("ulMyGNSSTypeID", c_ulong),
                ("dMyA0GGTO", c_double),
                ("dMyA1GGTO", c_double),
                ("dMyA2GGTO", c_double),
                ]


# noinspection PyTypeChecker
class GPSRAWCNAVMESSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMyPrn", c_ulong),
                ("ulMyFrameId", c_ulong),
                ("aucMyRawFrameData", c_char*38),
                ]


# noinspection PyTypeChecker
class CELLINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMake", c_char*20),
                ("szMyManufacturer", c_char*20),
                ("szMySerialNumber", c_char*32),
                ("szMySoftwareVersion", c_char*64),
                ("szMyMobileNumber", c_char*16),
                ("szMyMobileSubscriberId", c_char*32),
                ("szMyAccessPointName", c_char*100),
                ("szMyUsername", c_char*256),
                ("szMyPassword", c_char*256),
                ]


# noinspection PyTypeChecker
class CELLSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyModemStatus", c_uint),
                ("eMyNetStatus", c_uint),
                ("szMyIpAddress", c_char*16),
                ("iMySignal", c_int),
                ("iMyRssi", c_int),
                ("szMyNetwork", c_char*20),
                ("uiMyCellId", c_uint),
                ("iMyModemTemperature", c_int),
                ("szMyLastError", c_char*100),
                ]


# noinspection PyTypeChecker
class CAKEPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class CAKEXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ]


# noinspection PyTypeChecker
class CAKESATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class CAKESATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", CAKESATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class CAKETIME_clMySystemTimeOffsets_aclMySystemOffsets(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("dMyBias", c_double),
                ("dMyBiasStdDev", c_double),
                ]


# noinspection PyTypeChecker
class CAKETIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySystemTimeOffsets_aclMySystemOffsets_arraylength", c_ulong),
                ("clMySystemTimeOffsets_aclMySystemOffsets", CAKETIME_clMySystemTimeOffsets_aclMySystemOffsets*5),
                ]


# noinspection PyTypeChecker
class CAKEVEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class CAKEVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class SINGLEPOINTRESIDUALS_aclMyResiduals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyChannel", c_ulong),
                ("fMyResidual", c_float),
                ("fMyResidualStdDev", c_float),
                ]


# noinspection PyTypeChecker
class SINGLEPOINTRESIDUALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyResiduals_arraylength", c_ulong),
                ("aclMyResiduals", SINGLEPOINTRESIDUALS_aclMyResiduals*325),
                ]


# noinspection PyTypeChecker
class SINGLEPOINTOUTLIERS_aclMyOutliers(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyChannel", c_ulong),
                ("fMyMisclosure", c_float),
                ("fMyStdDev", c_float),
                ]


# noinspection PyTypeChecker
class SINGLEPOINTOUTLIERS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyOutliers_arraylength", c_ulong),
                ("aclMyOutliers", SINGLEPOINTOUTLIERS_aclMyOutliers*36),
                ]


# noinspection PyTypeChecker
class CAKELOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class QZSSRAWCNAVMESSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMyPrn", c_ulong),
                ("ulMyMessageId", c_ulong),
                ("aucMyRawFrameData", c_char*38),
                ]


# noinspection PyTypeChecker
class MODULEPOWER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyExtModule", c_uint),
                ("eMyOnOff", c_uint),
                ]


# noinspection PyTypeChecker
class GPSNAVCDC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTransmittingPRN", c_ulong),
                ("ulMyWNopd", c_ulong),
                ("ulMyTopd", c_ulong),
                ("ulMyTod", c_ulong),
                ("ulMyDataType", c_ulong),
                ("ulMyPRNa", c_ulong),
                ("dMyDeltaAf0", c_double),
                ("dMyDeltaAf1", c_double),
                ("dMyUDRA", c_double),
                ]


# noinspection PyTypeChecker
class GPSNAVEDC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTransmittingPRN", c_ulong),
                ("ulMyWNopd", c_ulong),
                ("ulMyTopd", c_ulong),
                ("ulMyTod", c_ulong),
                ("ulMyDataType", c_ulong),
                ("ulMyPRNa", c_ulong),
                ("dMyDeltaAlpha", c_double),
                ("dMyDeltaBeta", c_double),
                ("dMyDeltaGamma", c_double),
                ("dMyDeltaI", c_double),
                ("dMyDeltaOmega", c_double),
                ("dMyDeltaA", c_double),
                ("dMyDotUDRA", c_double),
                ]


# noinspection PyTypeChecker
class FAULT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class PPPPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PPPSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class PPPSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", PPPSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class PPPXYZ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyX", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyY", c_double),
                ("clMyCoords_clMyXYZ_clMyPosition_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyXYZ_clMyPosition_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyECEF_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyECEF_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PPPDOP2_clMyDOPs_aclMyTDOPs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("fMyDOP", c_float),
                ]


# noinspection PyTypeChecker
class PPPDOP2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyVDOP", c_float),
                ("clMyDOPs_aclMyTDOPs_arraylength", c_ulong),
                ("clMyDOPs_aclMyTDOPs", PPPDOP2_clMyDOPs_aclMyTDOPs*5),
                ]


# noinspection PyTypeChecker
class ORBITANDCLOCKCORRECTIONS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyIODE", c_ulong),
                ("clMyOrbitReferenceTime_ulMyMilliseconds", c_ulong),
                ("fMyXCorrection", c_float),
                ("fMyYCorrection", c_float),
                ("fMyZCorrection", c_float),
                ("fMyXCorrectionVelocity", c_float),
                ("fMyYCorrectionVelocity", c_float),
                ("fMyZCorrectionVelocity", c_float),
                ("clMyClockReferenceTime_ulMyMilliseconds", c_ulong),
                ("fMyClockCorrection", c_float),
                ("fMyClockCorrectionVelocity", c_float),
                ("fMyRangeStdDev", c_float),
                ]


# noinspection PyTypeChecker
class ORBITANDCLOCKCORRECTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_eMySource", c_uint),
                ("clMyProviderID_clMyInfo_szMyID", c_char*4),
                ("clMyInfo_ulMySolutionID", c_ulong),
                ("clMyInfo_ulMySSRIOD", c_ulong),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", ORBITANDCLOCKCORRECTIONS_aclMyEntries*72),
                ]


# noinspection PyTypeChecker
class PPPFILTERPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PPPEARTHTIDES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyModel", c_uint),
                ("dMyEastingCorrection", c_double),
                ("dMyNorthingCorrection", c_double),
                ("dMyHeightCorrection", c_double),
                ]


# noinspection PyTypeChecker
class PPPFASTRESIDUALS_aclMyDeltaPhaseResiduals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyResidual", c_float),
                ("fMyVariance", c_float),
                ]


# noinspection PyTypeChecker
class PPPFASTRESIDUALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseResiduals_arraylength", c_ulong),
                ("aclMyDeltaPhaseResiduals", PPPFASTRESIDUALS_aclMyDeltaPhaseResiduals*72),
                ]


# noinspection PyTypeChecker
class PPPRESIDUALS_aclMyResiduals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("idMyID", satelliteid),
                ("fMyResidual", c_float),
                ("fMyResidualStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PPPRESIDUALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignalType", c_uint),
                ("eMyObservationType", c_uint),
                ("fMyVarianceComponent", c_float),
                ("aclMyResiduals_arraylength", c_ulong),
                ("aclMyResiduals", PPPRESIDUALS_aclMyResiduals*22),
                ]


# noinspection PyTypeChecker
class PPPSYSTEMBIASES_aclMySystemBiases(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("fMyBias", c_float),
                ("fMyBiasStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PPPSYSTEMBIASES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySystemBiases_arraylength", c_ulong),
                ("aclMySystemBiases", PPPSYSTEMBIASES_aclMySystemBiases*4),
                ]


# noinspection PyTypeChecker
class PPPINTEGRITYEVENT_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyType", c_uint),
                ("fMyResidual", c_float),
                ("fMyStandardizedResidual", c_float),
                ]


# noinspection PyTypeChecker
class PPPINTEGRITYEVENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyGlobalThreshold", c_double),
                ("fMyGlobalStatistic", c_double),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", PPPINTEGRITYEVENT_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class PPPOUTLIERS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMySignalType", c_uint),
                ("eMyType", c_uint),
                ("fMyMisclosure", c_float),
                ]


# noinspection PyTypeChecker
class PPPOUTLIERS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", PPPOUTLIERS_aclMyEntries*325),
                ]


# noinspection PyTypeChecker
class GROUPDELAYS_aMyHLASSPosPoly(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyIOD", c_ulong),
                ("dMyTGD", c_double),
                ]


# noinspection PyTypeChecker
class GROUPDELAYS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aMyHLASSPosPoly_arraylength", c_ulong),
                ("aMyHLASSPosPoly", GROUPDELAYS_aMyHLASSPosPoly*319),
                ]


# noinspection PyTypeChecker
class PPPLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class BDSB1RAWNAVSUBFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySignalChannelNumber", c_ulong),
                ("ulMySatelliteID", c_ulong),
                ("ulMySubframeID", c_ulong),
                ("aucMyRawSubframeData", c_char*28),
                ]


# noinspection PyTypeChecker
class RTCAREFPVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMyNovAtelDesignator", c_char),
                ("ucMySubTypeIndicator", c_char),
                ("ulMyWeek", c_ulong),
                ("dMyRTCATime", c_double),
                ("clMyRelativePVAInfo_dMyUserPosX", c_double),
                ("clMyRelativePVAInfo_dMyUserPosY", c_double),
                ("clMyRelativePVAInfo_dMyUserPosZ", c_double),
                ("clMyRelativePVAInfo_dMyUserVelE", c_double),
                ("clMyRelativePVAInfo_dMyUserVelN", c_double),
                ("clMyRelativePVAInfo_dMyUserVelU", c_double),
                ("clMyRelativePVAInfo_dMyRoll", c_double),
                ("clMyRelativePVAInfo_dMyPitch", c_double),
                ("clMyRelativePVAInfo_dMyAzimuth", c_double),
                ("clMyRelativePVAInfo_ucMyVelType", c_char),
                ("clMyRelativePVAInfo_ucMyINSStatus", c_char),
                ("clMyRelativePVAInfo_ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class RTCAREFPVAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeader_ulMessageIdentifier", c_ulong),
                ("clMyHeader_ulRefStation", c_ulong),
                ("clMyHeader_ulMessageType", c_ulong),
                ("clMyHeader_ulReserved", c_ulong),
                ("clMyHeader_ulMessageLength", c_ulong),
                ("ucMyNovAtelDesignator", c_char),
                ("ucMySubTypeIndicator", c_char),
                ("ulMyWeek", c_ulong),
                ("dMyRTCATime", c_double),
                ("clMyRelativePVAInfo_dMyUserPosX", c_double),
                ("clMyRelativePVAInfo_dMyUserPosY", c_double),
                ("clMyRelativePVAInfo_dMyUserPosZ", c_double),
                ("clMyRelativePVAInfo_dMyUserVelE", c_double),
                ("clMyRelativePVAInfo_dMyUserVelN", c_double),
                ("clMyRelativePVAInfo_dMyUserVelU", c_double),
                ("clMyRelativePVAInfo_dMyRoll", c_double),
                ("clMyRelativePVAInfo_dMyPitch", c_double),
                ("clMyRelativePVAInfo_dMyAzimuth", c_double),
                ("clMyRelativePVAInfo_ucMyVelType", c_char),
                ("clMyRelativePVAInfo_ucMyINSStatus", c_char),
                ("clMyRelativePVAInfo_ucMyReserved", c_char),
                ]


# noinspection PyTypeChecker
class RELINSPVAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRelINSPVAInfo_eMyRelINSOutput", c_uint),
                ("clMyRelINSPVAInfo_dMyDeltaPosN", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPosE", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPosU", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelN", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelE", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelU", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaRoll", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPitch", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaHeading", c_double),
                ("clMyRelINSPVAInfo_fMyDifferentialLag", c_float),
                ("clMyRelINSPVAInfo_acMyRoverID", c_char*4),
                ("clMyRelINSPVAInfo_eMyRoverINSStatus", c_uint),
                ("clMyRelINSPVAInfo_acMyMasterID", c_char*4),
                ("clMyRelINSPVAInfo_eMyMasterINSStatus", c_uint),
                ("clMyRelINSPVAInfo_eMyRTKBaselineStatus", c_uint),
                ("clMyRelINSPVAInfo_ulMyExtendedSolStat", c_ulong),
                ]


# noinspection PyTypeChecker
class USERACCOUNTS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyUserName", c_char*32),
                ]


# noinspection PyTypeChecker
class BDSB1EPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyWN", c_ulong),
                ("dMyURA", c_double),
                ("ulMySatH1", c_ulong),
                ("dMyTGD1", c_double),
                ("ulMyIODC", c_ulong),
                ("ulMyTOC", c_ulong),
                ("dMyA0", c_double),
                ("dMyA1", c_double),
                ("dMyA2", c_double),
                ("ulMyIODE", c_ulong),
                ("ulMyTOE", c_ulong),
                ("dMyRootA", c_double),
                ("dMyEccentricity", c_double),
                ("dMyOmega", c_double),
                ("dMyDeltaN", c_double),
                ("dMyM0", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyI0", c_double),
                ("dMyIDot", c_double),
                ("dMyCuc", c_double),
                ("dMyCus", c_double),
                ("dMyCrc", c_double),
                ("dMyCrs", c_double),
                ("dMyCic", c_double),
                ("dMyCis", c_double),
                ]


# noinspection PyTypeChecker
class BDSALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyWN", c_ulong),
                ("ulMyTOA", c_ulong),
                ("dMyRootA", c_double),
                ("dMyEccentricity", c_double),
                ("dMyOmega", c_double),
                ("dMyM0", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyDeltaI", c_double),
                ("dMyA0", c_double),
                ("dMyA1", c_double),
                ("ulMyHealth", c_ulong),
                ]


# noinspection PyTypeChecker
class BDSALMANACHEALTH_aclMyHealths(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySatelliteID", c_ushort),
                ("usMyHealth", c_ushort),
                ]


# noinspection PyTypeChecker
class BDSALMANACHEALTH(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySourceSatelliteID", c_ulong),
                ("ulMyWN", c_ulong),
                ("ulMyTOA", c_ulong),
                ("aclMyHealths_arraylength", c_ulong),
                ("aclMyHealths", BDSALMANACHEALTH_aclMyHealths*30),
                ]


# noinspection PyTypeChecker
class BDSIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTransmittingSatelliteID", c_ulong),
                ("dMyAlpha0", c_double),
                ("dMyAlpha1", c_double),
                ("dMyAlpha2", c_double),
                ("dMyAlpha3", c_double),
                ("dMyBeta0", c_double),
                ("dMyBeta1", c_double),
                ("dMyBeta2", c_double),
                ("dMyBeta3", c_double),
                ]


# noinspection PyTypeChecker
class RTCM4093TYPE5(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1121(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1122(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1123(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1124(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1125(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1126(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1127(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class NOVATELXGPSOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class NOVATELXGLOOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class NOVATELXSBASOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class NOVATELXGALOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class NOVATELXQZSSOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class NOVATELXBDSOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class BDSCLOCK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyA0UTC", c_double),
                ("dMyA1UTC", c_double),
                ("sMyDeltaTls", c_short),
                ("usMyWNlsf", c_ushort),
                ("usMyDN", c_ushort),
                ("sMyDeltaTlsf", c_short),
                ("dMyA0GPS", c_double),
                ("dMyA1GPS", c_double),
                ("dMyA0Gal", c_double),
                ("dMyA1Gal", c_double),
                ("dMyA0GLO", c_double),
                ("dMyA1GLO", c_double),
                ]


# noinspection PyTypeChecker
class BLUETOOTHSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyBluetoothStatus", c_uint),
                ("sMyBluetoothInfo", c_char*272),
                ("sMyBluetoothInfo1", c_char*64),
                ("sMyBluetoothInfo2", c_char*64),
                ("ulMyUpgradeProgress", c_ulong),
                ]


# noinspection PyTypeChecker
class WIFICLISTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyState", c_uint),
                ("sMyMacAddress", c_char*20),
                ("bMyIsScanInProgresss", c_bool),
                ("fMyLinkSpeed", c_float),
                ("fMyLinkSpeedMax", c_float),
                ("eMyNetworkId", c_uint),
                ("clMyBssInfo_clMyNetworkInfo_sMySSID", c_char*36),
                ("clMyBssInfo_clMyNetworkInfo_sMyBSSID", c_char*20),
                ("clMyBssInfo_clMyNetworkInfo_sMyFrequencyBand", c_char*16),
                ("clMyBssInfo_clMyNetworkInfo_uiMyChannel", c_uint),
                ("clMyNetworkInfo_iMyRSSI", c_int),
                ("eMyError", c_uint),
                ("ulMyErrorCode", c_ulong),
                ]


# noinspection PyTypeChecker
class WIFICLISCANRESULTS_aclMyNetworks(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBssInfo_eMyBssType", c_uint),
                ("clMyBssInfo_sMySSID", c_char*36),
                ("clMyBssInfo_sMyBSSID", c_char*20),
                ("clMyBssInfo_sMyAuthenticationType", c_char*32),
                ("clMyBssInfo_sMyEncryptionProtocol", c_char*32),
                ("clMyBssInfo_sMyFrequencyBand", c_char*16),
                ("clMyBssInfo_uiMyChannel", c_uint),
                ("clMyBssInfo_usMyNonHtRates", c_ushort),
                ("clMyBssInfo_aulMyHtRates", c_ulong*3),
                ("iMyRSSI", c_int),
                ]


# noinspection PyTypeChecker
class WIFICLISCANRESULTS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyNetworks_arraylength", c_ulong),
                ("aclMyNetworks", WIFICLISCANRESULTS_aclMyNetworks*50),
                ]


# noinspection PyTypeChecker
class NOVATELXOBS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*2800),
                ]


# noinspection PyTypeChecker
class NOVATELXOBSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*2800),
                ]


# noinspection PyTypeChecker
class NOVATELXREF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*800),
                ]


# noinspection PyTypeChecker
class NOVATELXREFIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*800),
                ]


# noinspection PyTypeChecker
class PPPTROPODELAYS_aclMyTroposphereDelays(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyDelay", c_float),
                ("fMyDelayStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PPPTROPODELAYS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyTroposphereDelays_arraylength", c_ulong),
                ("aclMyTroposphereDelays", PPPTROPODELAYS_aclMyTroposphereDelays*72),
                ]


# noinspection PyTypeChecker
class DEBUGDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucBuffer", c_char*4096),
                ]


# noinspection PyTypeChecker
class NOVATELXREFTEMP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRTCMV3REF_MessageNumber", c_ushort),
                ("clMyRTCMV3REF_NovatelXStationID", c_ushort),
                ("clMyRTCMV3REF_ITRFRealizationYear", c_char),
                ("clMyRTCMV3REF_GPSIndicator", c_char),
                ("clMyRTCMV3REF_GLONASSIndicator", c_char),
                ("clMyRTCMV3REF_GalileoIndicator", c_char),
                ("clMyRTCMV3REF_ReferenceStationIndicator", c_char),
                ("clMyRTCMV3REF_ECEFX", c_double),
                ("clMyRTCMV3REF_SingleReceiverOscIndicator", c_char),
                ("clMyRTCMV3REF_Reserved", c_char),
                ("clMyRTCMV3REF_ECEFY", c_double),
                ("clMyRTCMV3REF_QuarterCycleIndicator", c_char),
                ("clMyRTCMV3REF_ECEFZ", c_double),
                ("clMyRTCMV3REF_AntennaHeight", c_ushort),
                ]


# noinspection PyTypeChecker
class RTCM1104BDS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1101(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1102(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1103(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1104(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1105(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1106(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1107(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1111(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1112(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1113(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1114(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1115(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1116(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1117(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*901),
                ]


# noinspection PyTypeChecker
class RTCM1230(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("uiMyMessageNumber", c_ushort),
                ("uiMyReferenceStationID", c_ushort),
                ("ucMyGLOCPBiasIndicator", c_char),
                ("ucMyReserved", c_char),
                ("ucMySignalMask", c_char),
                ("sMyL1CABias", c_short),
                ("sMyL1PBias", c_short),
                ("sMyL2CABias", c_short),
                ("sMyL2PBias", c_short),
                ]


# noinspection PyTypeChecker
class RTCM1230IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyMessageNumber", c_short),
                ("uiMyReferenceStationID", c_ushort),
                ("ucMyGLOCPBiasIndicator", c_char),
                ("ucMyReserved", c_char),
                ("ucMySignalMask", c_char),
                ("sMyL1CABias", c_short),
                ("sMyL1PBias", c_short),
                ("sMyL2CABias", c_short),
                ("sMyL2PBias", c_short),
                ]


# noinspection PyTypeChecker
class HEADING3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMyHeadingInfo_fMyHeadingStdDev", c_float),
                ("clMyHeadingInfo_fMyPitchStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class DEBUGVAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyRestartCount", c_ulong),
                ("szMyAsName", c_char*64),
                ("szMyTaskName", c_char*64),
                ("lMyErr", c_long),
                ("lMyLineNumber", c_long),
                ("ulMyPC", c_ulong),
                ]


# noinspection PyTypeChecker
class HEADINGEXT2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeadingExtInfo_acMyRoverId", c_char*4),
                ("clMyHeadingExtInfo_acMyMasterId", c_char*4),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*512),
                ]


# noinspection PyTypeChecker
class HEADINGEXT2IN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeadingExtInfo_acMyRoverId", c_char*4),
                ("clMyHeadingExtInfo_acMyMasterId", c_char*4),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*512),
                ]


# noinspection PyTypeChecker
class WIFIAPSTATUS_aclMyStationInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sMyMacAddress", c_char*20),
                ("fMyLinkSpeed", c_float),
                ]


# noinspection PyTypeChecker
class WIFIAPSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyState", c_uint),
                ("sMyBSSID", c_char*20),
                ("eMyApId", c_uint),
                ("aclMyStationInfo_arraylength", c_ulong),
                ("aclMyStationInfo", WIFIAPSTATUS_aclMyStationInfo*10),
                ]


# noinspection PyTypeChecker
class BESTPOSIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class HWCONFIGTABLERAW_clMyHWConfigTableEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyType", c_char),
                ("usMyData", c_ushort),
                ]


# noinspection PyTypeChecker
class HWCONFIGTABLERAW(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNumClearedPackets", c_ulong),
                ("ulMyNumUnusedPackets", c_ulong),
                ("clMyHWConfigTableEntries_arraylength", c_ulong),
                ("clMyHWConfigTableEntries", HWCONFIGTABLERAW_clMyHWConfigTableEntries*125),
                ]


# noinspection PyTypeChecker
class IPSTATS_aclMyIpInterfaceStatistics(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPhysicalInterface", c_uint),
                ("ulMyConnectionDuration", c_ulong),
                ("ulMyRxCount", c_ulong),
                ("ulMyTxCount", c_ulong),
                ]


# noinspection PyTypeChecker
class IPSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyIpInterfaceStatistics_arraylength", c_ulong),
                ("aclMyIpInterfaceStatistics", IPSTATS_aclMyIpInterfaceStatistics*24),
                ]


# noinspection PyTypeChecker
class BLUETOOTHDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucBuffer_Len", c_ulong),
                ("aucBuffer", c_char*100),
                ]


# noinspection PyTypeChecker
class PPPTROPOMODEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyZenithTropoTotalDelay", c_float),
                ("fMyZenithTropoResidualDelay", c_float),
                ("fMyZenithTropoResidualDelayStdDev", c_float),
                ]


# noinspection PyTypeChecker
class CELLULARSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyModemStatus", c_uint),
                ("eMyNetStatus", c_uint),
                ("szMyIpAddress", c_char*16),
                ("iMySignal", c_int),
                ("iMyRssi", c_int),
                ("szMyNetwork", c_char*20),
                ("uiMyCellId", c_uint),
                ("iMyModemTemperature", c_int),
                ("szMyLastError", c_char*100),
                ]


# noinspection PyTypeChecker
class CELLULARINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMake", c_char*20),
                ("szMyManufacturer", c_char*20),
                ("szMySerialNumber", c_char*32),
                ("szMySoftwareVersion", c_char*64),
                ("szMyMobileNumber", c_char*16),
                ("szMyMobileSubscriberId", c_char*32),
                ]


# noinspection PyTypeChecker
class BDSRAWNAVSUBFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySignalChannelNumber", c_ulong),
                ("ulMySatelliteID", c_ulong),
                ("eMyBDSDataSource", c_uint),
                ("ulMySubframeID", c_ulong),
                ("aucMyRawSubframeData", c_char*28),
                ]


# noinspection PyTypeChecker
class BDSEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("ulMyWN", c_ulong),
                ("dMyURA", c_double),
                ("ulMySatH1", c_ulong),
                ("dMyTGD1", c_double),
                ("dMyTGD2", c_double),
                ("ulMyIODC", c_ulong),
                ("ulMyTOC", c_ulong),
                ("dMyA0", c_double),
                ("dMyA1", c_double),
                ("dMyA2", c_double),
                ("ulMyIODE", c_ulong),
                ("ulMyTOE", c_ulong),
                ("dMyRootA", c_double),
                ("dMyEccentricity", c_double),
                ("dMyOmega", c_double),
                ("dMyDeltaN", c_double),
                ("dMyM0", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyI0", c_double),
                ("dMyIDot", c_double),
                ("dMyCuc", c_double),
                ("dMyCus", c_double),
                ("dMyCrc", c_double),
                ("dMyCrs", c_double),
                ("dMyCic", c_double),
                ("dMyCis", c_double),
                ]


# noinspection PyTypeChecker
class DEBUGROUTETABLE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szRouteTable", c_char*2048),
                ]


# noinspection PyTypeChecker
class HEADINGRATE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeadingRate_eMySolutionStatus", c_uint),
                ("clMyHeadingRate_eMySolutionType", c_uint),
                ("clMyHeadingRate_fMyLatency", c_float),
                ("clMyRates_clMyHeadingRate_fMyBLength", c_float),
                ("clMyRates_clMyHeadingRate_fMyHeading", c_float),
                ("clMyRates_clMyHeadingRate_fMyPitch", c_float),
                ("clMyRates_clMyHeadingRate_fMyBLengthStdDev", c_float),
                ("clMyRates_clMyHeadingRate_fMyHeadingStdDev", c_float),
                ("clMyRates_clMyHeadingRate_fMyPitchStdDev", c_float),
                ("fFloat", c_float),
                ("acMyRoverID", c_char*4),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ]


# noinspection PyTypeChecker
class SYNCHEAVE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeaveInfo_dMyHeave", c_double),
                ("clMyHeaveInfo_dMyHeaveStdev", c_double),
                ]


# noinspection PyTypeChecker
class DELAYEDHEAVE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyHeaveInfo_dMyHeave", c_double),
                ("clMyHeaveInfo_dMyHeaveStdev", c_double),
                ]


# noinspection PyTypeChecker
class VERIPOSDEBUGDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyData_Len", c_ulong),
                ("acMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class PPPSEEDSTORE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMode", c_uint),
                ("dMyLatitudeInDegrees", c_double),
                ("dMyLongitudeInDegrees", c_double),
                ("dMyEllipsoidalHeight", c_double),
                ("dMyNorthingStdDev", c_double),
                ("dMyEastingStdDev", c_double),
                ("dMyHeightStdDev", c_double),
                ("dMyNorthingEastingCovariance", c_double),
                ("dMyNorthingHeightCovariance", c_double),
                ("dMyEastingHeightCovariance", c_double),
                ]


# noinspection PyTypeChecker
class RTCMV2DATAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyVariableMessage_Len", c_ulong),
                ("aucMyVariableMessage", c_char*1023),
                ]


# noinspection PyTypeChecker
class RTCMV3DATAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class NOVATELXRTCMV3SSRIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class LBANDBEAMTABLE_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyName", c_char*8),
                ("acMyRegionID", c_char*8),
                ("ulMyFrequencyInHz", c_ulong),
                ("ulMyBaudRate", c_ulong),
                ("fMyLongitude", c_float),
                ("ulMyBeamAccess", c_ulong),
                ]


# noinspection PyTypeChecker
class LBANDBEAMTABLE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", LBANDBEAMTABLE_aclMyEntries*32),
                ]


# noinspection PyTypeChecker
class TERRASTARINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyPAC", c_char*16),
                ("clMyTerrastarServiceInfo_eMyOperatingMode", c_uint),
                ("clMyTerrastarServiceInfo_ulMySubscriptionDetails", c_ulong),
                ("clMyTerrastarServiceInfo_ulMyContractEndDayOfYear", c_ulong),
                ("clMyTerrastarServiceInfo_ulMyContractEndYear", c_ulong),
                ("clMyTerrastarServiceInfo_ulMyTimedEnablePeriod", c_ulong),
                ("clMyTerrastarServiceInfo_eMyRegionRestriction", c_uint),
                ("clMyTerrastarServiceInfo_fMyLocalAreaCenterPointLatitude", c_float),
                ("clMyTerrastarServiceInfo_fMyLocalAreaCenterPointLongitude", c_float),
                ("clMyTerrastarServiceInfo_ulMyLocalAreaRadius", c_ulong),
                ]


# noinspection PyTypeChecker
class PPPFILTERSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class PPPFILTERSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", PPPFILTERSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class VERIPOSMESSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage_Len", c_ulong),
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class VERIPOSRTCMDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStream", c_ulong),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class VERIPOSMESSAGETYPES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aulMyAllowedMessageTypes_Len", c_ulong),
                ("aulMyAllowedMessageTypes", c_ulong*50),
                ]


# noinspection PyTypeChecker
class VERIPOSSTANDARDSTATIONS_aclMyStations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyID", c_ulong),
                ("fMyLatitude", c_float),
                ("fMyLongitude", c_float),
                ("eMyHealth", c_uint),
                ]


# noinspection PyTypeChecker
class VERIPOSSTANDARDSTATIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyStations_arraylength", c_ulong),
                ("aclMyStations", VERIPOSSTANDARDSTATIONS_aclMyStations*100),
                ]


# noinspection PyTypeChecker
class VERIPOSINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySerialNumber", c_ulong),
                ("clMyVeriposServiceInfo_eMyOperatingMode", c_uint),
                ("clMyVeriposServiceInfo_ulMySubscriptionDetails", c_ulong),
                ("szMyServiceCode", c_char*4),
                ]


# noinspection PyTypeChecker
class TERRASTARSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyAccessStatus", c_uint),
                ("eMyDecoderSyncState", c_uint),
                ("ulMyTimedEnableRemainingTime", c_ulong),
                ("eMyLocalAreaStatus", c_uint),
                ("eMyGeogatingStatus", c_uint),
                ]


# noinspection PyTypeChecker
class VERIPOSSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyAccessStatus", c_uint),
                ("eMyDecoderSyncState", c_uint),
                ]


# noinspection PyTypeChecker
class VERIPOSEXTENDEDINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyDecoderVersion", c_char*20),
                ("ulMySerialNumber", c_ulong),
                ("szMyPAC", c_char*16),
                ("szMySubscriptionString", c_char*512),
                ("szMyServiceControlString", c_char*512),
                ]


# noinspection PyTypeChecker
class DEBUGTXBUFFERS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPortId", c_uint),
                ("ulMyLowBufferSpaceLeft", c_ulong),
                ("ulMyLowSpaceLeftMinimum", c_ulong),
                ("ulMyHighBufferSpaceLeft", c_ulong),
                ("ulMyHighSpaceLeftMinimum", c_ulong),
                ]


# noinspection PyTypeChecker
class RANGECMP3(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyRangeData_Len", c_ulong),
                ("aucMyRangeData", c_char*16250),
                ]


# noinspection PyTypeChecker
class VERIPOSNVMDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMyBlockId", c_int),
                ("ulMySavedByVersion", c_ulong),
                ("iMyLength", c_int),
                ("aucMyBuf", c_char*1024),
                ]


# noinspection PyTypeChecker
class MARK3POS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class MARK4POS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class SYNCRELINSPVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyRelINSPVAInfo_eMyRelINSOutput", c_uint),
                ("clMyRelINSPVAInfo_dMyDeltaPosN", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPosE", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPosU", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelN", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelE", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaVelU", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaRoll", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaPitch", c_double),
                ("clMyRelINSPVAInfo_dMyDeltaHeading", c_double),
                ("clMyRelINSPVAInfo_fMyDifferentialLag", c_float),
                ("clMyRelINSPVAInfo_acMyRoverID", c_char*4),
                ("clMyRelINSPVAInfo_eMyRoverINSStatus", c_uint),
                ("clMyRelINSPVAInfo_acMyMasterID", c_char*4),
                ("clMyRelINSPVAInfo_eMyMasterINSStatus", c_uint),
                ("clMyRelINSPVAInfo_eMyRTKBaselineStatus", c_uint),
                ("clMyRelINSPVAInfo_ulMyExtendedSolStat", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGPROCESSRUNTIMES_aclMyRunTimes(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyProcessID", c_ulong),
                ("szMyProcessName", c_char*100),
                ("ulMyRunTimeCount", c_ulong),
                ("fMyRunTimePercent", c_float),
                ]


# noinspection PyTypeChecker
class DEBUGPROCESSRUNTIMES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyRunTimes_arraylength", c_ulong),
                ("aclMyRunTimes", DEBUGPROCESSRUNTIMES_aclMyRunTimes*32),
                ]


# noinspection PyTypeChecker
class EM3000(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyHeaveInfo_dMyHeave", c_double),
                ]


# noinspection PyTypeChecker
class TRACKSUMMARY_aclMyTrackedGNSS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("ulMyNumTracked", c_ulong),
                ]


# noinspection PyTypeChecker
class TRACKSUMMARY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("ulMyTotalSatsTracked", c_ulong),
                ("aclMyTrackedGNSS_arraylength", c_ulong),
                ("aclMyTrackedGNSS", TRACKSUMMARY_aclMyTrackedGNSS*32),
                ]


# noinspection PyTypeChecker
class PPPSEEDSIGNALS_aclMyDeltaPhaseSeedSignals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("dMyPseudorange", c_double),
                ("dMyPhaseRange", c_double),
                ("fMyPhaseRangeStdDev", c_float),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ("eMySignal", c_uint),
                ]


# noinspection PyTypeChecker
class PPPSEEDSIGNALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseSeedSignals_arraylength", c_ulong),
                ("aclMyDeltaPhaseSeedSignals", PPPSEEDSIGNALS_aclMyDeltaPhaseSeedSignals*325),
                ]


# noinspection PyTypeChecker
class PPPDETECTEDDYNAMICS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDetectedDynamics", c_uint),
                ("fMyHorizontalSpeed", c_float),
                ("fMyVerticalSpeed", c_float),
                ("bMyIsCreepDetected", c_bool),
                ]


# noinspection PyTypeChecker
class PPPFASTLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class PPPFASTGROSSOUTLIERS_aclMyGrossOutlierSatelliteIDs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("idMyID", satelliteid),
                ]


# noinspection PyTypeChecker
class PPPFASTGROSSOUTLIERS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyGrossOutlierSatelliteIDs_arraylength", c_ulong),
                ("aclMyGrossOutlierSatelliteIDs", PPPFASTGROSSOUTLIERS_aclMyGrossOutlierSatelliteIDs*12),
                ]


# noinspection PyTypeChecker
class PPPVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class PPPVEL2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_fMyZStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class DEBUGPROCESSMEMUSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyProcessID", c_ulong),
                ("ulMyNumAllocations", c_ulong),
                ("ulMyNumDeallocations", c_ulong),
                ("ulMyTotalMemRequested", c_ulong),
                ("ulMyTotalMemDeallocated", c_ulong),
                ("ulMyTotalMemAllocated", c_ulong),
                ("ulMyMaxMemAllocated", c_ulong),
                ("szMyProcessName", c_char*100),
                ]


# noinspection PyTypeChecker
class GENERATEINSALIGNCORRECTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("ulMyBaudRate", c_ulong),
                ("ulMyObsRateInHz", c_ulong),
                ("ulMyRefRateInHz", c_ulong),
                ("eMyCorrectionInterface", c_uint),
                ]


# noinspection PyTypeChecker
class GPHCD(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCMonth", c_char),
                ("ulUTCYear", c_ulong),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("clMyVelocity_dMyHorizontalSpeed", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("dMyEasting", c_double),
                ("dMyNorthing", c_double),
                ("ulMyGGAQuality", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ]


# noinspection PyTypeChecker
class BDXT1(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulUTCYear", c_ulong),
                ("ucUTCMonth", c_char),
                ("ucUTCDay", c_char),
                ("dMyNorthing", c_double),
                ("dMyEasting", c_double),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyVelocity_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_dMyGroundTrack", c_double),
                ]


# noinspection PyTypeChecker
class PTNL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucUTCDay", c_char),
                ("ucUTCMonth", c_char),
                ("ulUTCYear", c_ulong),
                ("dMyNorthing", c_double),
                ("dMyEasting", c_double),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ]


# noinspection PyTypeChecker
class GPTRA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("ulMyGGAQuality", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ]


# noinspection PyTypeChecker
class GPNTR(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ("clMyENUBaseline_dMyEast", c_double),
                ("clMyENUBaseline_dMyNorthing", c_double),
                ("clMyENUBaseline_dMyUp", c_double),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("ulMyGGAQuality", c_ulong),
                ]


# noinspection PyTypeChecker
class UPTIME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyUptime", c_ulong),
                ]


# noinspection PyTypeChecker
class IMURATEPVA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class RTKFASTLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class BESTSEEDPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class STEADYLINESTATE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBias_clMyInterEngineState_dMyX", c_double),
                ("clMyBias_clMyInterEngineState_dMyY", c_double),
                ("clMyBias_clMyInterEngineState_dMyZ", c_double),
                ("clMyStdDevRatio_clMyInterEngineState_dMyX", c_double),
                ("clMyStdDevRatio_clMyInterEngineState_dMyY", c_double),
                ("clMyStdDevRatio_clMyInterEngineState_dMyZ", c_double),
                ("clMyBiasVariance_clMyInterEngineState_dMyX", c_double),
                ("clMyBiasVariance_clMyInterEngineState_dMyY", c_double),
                ("clMyBiasVariance_clMyInterEngineState_dMyZ", c_double),
                ("clMyInterEngineState_fMyUndulationBias", c_float),
                ("clMyInterEngineState_dMyTransitionTime", c_double),
                ("clMyInterEngineState_bMyIsInTransition", c_bool),
                ("clMyInterEngineState_eMyUnderlyingSource", c_uint),
                ]


# noinspection PyTypeChecker
class STEADYLINEINTERNALSTATE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBias_clMyIntraEngineState_dMyX", c_double),
                ("clMyBias_clMyIntraEngineState_dMyY", c_double),
                ("clMyBias_clMyIntraEngineState_dMyZ", c_double),
                ("clMyStdDevRatio_clMyIntraEngineState_dMyX", c_double),
                ("clMyStdDevRatio_clMyIntraEngineState_dMyY", c_double),
                ("clMyStdDevRatio_clMyIntraEngineState_dMyZ", c_double),
                ("clMyBiasVariance_clMyIntraEngineState_dMyX", c_double),
                ("clMyBiasVariance_clMyIntraEngineState_dMyY", c_double),
                ("clMyBiasVariance_clMyIntraEngineState_dMyZ", c_double),
                ("clMyIntraEngineState_fMyUndulationBias", c_float),
                ("clMyIntraEngineState_dMyTransitionTime", c_double),
                ("clMyIntraEngineState_bMyIsInTransition", c_bool),
                ("clMyIntraEngineState_eMyUnderlyingSource", c_uint),
                ]


# noinspection PyTypeChecker
class DEBUGCONTEXTSWITCH(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySwitchCount", c_ulong),
                ("ulMySwitchAverageTicks", c_ulong),
                ("ulMyFIQDuringCB", c_ulong),
                ("ulMyIRQDuringCB", c_ulong),
                ]


# noinspection PyTypeChecker
class ALIGNSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySolutionStatus", c_uint),
                ("eMySolutionType", c_uint),
                ("acMyRoverID", c_char*4),
                ("acMyMasterID", c_char*4),
                ("fMyUnitVariance", c_float),
                ("fMyMaxExternalReliability", c_float),
                ("clMyLLHStdWRTBase_fMyLatStdDev", c_float),
                ("clMyLLHStdWRTBase_fMyLongStdDev", c_float),
                ("clMyLLHStdWRTBase_fMyHgtStdDev", c_float),
                ("dMyLatitudeLongitudeCovariance", c_double),
                ("dMyLatitudeUpCovariance", c_double),
                ("dMyLongitudeUpCovariance", c_double),
                ("ucMyMeasurementSource", c_char),
                ("fFloat", c_float),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ]


# noinspection PyTypeChecker
class PAVSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPAVStatusData_eMyPAVTaskStatus", c_uint),
                ("clMyPAVStatusData_eMyPAVRollStatus", c_uint),
                ("clMyPAVStatusData_eMyPAVPitchStatus", c_uint),
                ("clMyPAVStatusData_eMyPAVAzimuthStatus", c_uint),
                ("clMyPAVStatusData_eMyPAVGroundTrackStatus", c_uint),
                ("clMyPAVStatusData_bMyIsGimbalActive", c_bool),
                ]


# noinspection PyTypeChecker
class RTKSEEDSIGNALS_aclMyDeltaPhaseSeedSignals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("dMyPseudorange", c_double),
                ("dMyPhaseRange", c_double),
                ("fMyLockTime", c_float),
                ("ulMyCStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class RTKSEEDSIGNALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseSeedSignals_arraylength", c_ulong),
                ("aclMyDeltaPhaseSeedSignals", RTKSEEDSIGNALS_aclMyDeltaPhaseSeedSignals*325),
                ]


# noinspection PyTypeChecker
class RTKFASTRESIDUALS_aclMyDeltaPhaseResiduals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyResidual", c_float),
                ("fMyVariance", c_float),
                ]


# noinspection PyTypeChecker
class RTKFASTRESIDUALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseResiduals_arraylength", c_ulong),
                ("aclMyDeltaPhaseResiduals", RTKFASTRESIDUALS_aclMyDeltaPhaseResiduals*60),
                ]


# noinspection PyTypeChecker
class RTKFASTIONO_aclMyDeltaPhaseIonosphereFilters(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyIonosphereRate", c_float),
                ("fMyIonosphereRateVariance", c_float),
                ("fMyObservedIonosphereRate", c_float),
                ]


# noinspection PyTypeChecker
class RTKFASTIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseIonosphereFilters_arraylength", c_ulong),
                ("aclMyDeltaPhaseIonosphereFilters", RTKFASTIONO_aclMyDeltaPhaseIonosphereFilters*72),
                ]


# noinspection PyTypeChecker
class RTKBASEIONO_aclMyDeltaPhaseIonosphereFilters(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyIonosphereRate", c_float),
                ("fMyIonosphereRateVariance", c_float),
                ("fMyObservedIonosphereRate", c_float),
                ]


# noinspection PyTypeChecker
class RTKBASEIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseIonosphereFilters_arraylength", c_ulong),
                ("aclMyDeltaPhaseIonosphereFilters", RTKBASEIONO_aclMyDeltaPhaseIonosphereFilters*72),
                ]


# noinspection PyTypeChecker
class RTKBASESATELLITECLOCKS_aclMySatelliteClockRates(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyFilteredRate", c_float),
                ("fMyFilteredRateStdDev", c_float),
                ("fMyObservedRate", c_float),
                ]


# noinspection PyTypeChecker
class RTKBASESATELLITECLOCKS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySatelliteClockRates_arraylength", c_ulong),
                ("aclMySatelliteClockRates", RTKBASESATELLITECLOCKS_aclMySatelliteClockRates*72),
                ]


# noinspection PyTypeChecker
class RTKBASELOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class PDPFASTLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class PDPFASTIONO_aclMyDeltaPhaseIonosphereFilters(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyIonosphereRate", c_float),
                ("fMyIonosphereRateVariance", c_float),
                ("fMyObservedIonosphereRate", c_float),
                ]


# noinspection PyTypeChecker
class PDPFASTIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseIonosphereFilters_arraylength", c_ulong),
                ("aclMyDeltaPhaseIonosphereFilters", PDPFASTIONO_aclMyDeltaPhaseIonosphereFilters*72),
                ]


# noinspection PyTypeChecker
class PDPFILTERPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("cCharAsInt", c_char),
                ("cCharAsInt", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class PDPFASTRESIDUALS_aclMyDeltaPhaseResiduals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyResidual", c_float),
                ("fMyVariance", c_float),
                ]


# noinspection PyTypeChecker
class PDPFASTRESIDUALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseResiduals_arraylength", c_ulong),
                ("aclMyDeltaPhaseResiduals", PDPFASTRESIDUALS_aclMyDeltaPhaseResiduals*72),
                ]


# noinspection PyTypeChecker
class PDPFILTERSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ("ulMyStatusMask", c_ulong),
                ]


# noinspection PyTypeChecker
class PDPFILTERSATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", PDPFILTERSATS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ]


# noinspection PyTypeChecker
class CELLULARACTIVATESTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyStatus", c_char*64),
                ("szMyError", c_char*128),
                ("szMyReserved", c_char*32),
                ]


# noinspection PyTypeChecker
class CELLULARIPSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNetworkId", c_ulong),
                ("eMyDataRegStatus", c_uint),
                ("bMyIPConn", c_bool),
                ("eMyAccessTechnology", c_uint),
                ("uiMyCellID", c_uint),
                ("iMyRac", c_int),
                ("uiMyCDMADataRetryCount", c_uint),
                ("szMyIpAddress", c_char*16),
                ("szMyNetmask", c_char*16),
                ("szMyGateway", c_char*16),
                ("szMyDns1", c_char*16),
                ("szMyDns2", c_char*16),
                ("uiMyTxBytes", c_uint),
                ("uiMyRxBytes", c_uint),
                ("ulNoOfIpDisconnections", c_ulong),
                ("iMyReserved1", c_int),
                ("iMyReserved2", c_int),
                ("fMyReserved3", c_float),
                ("fMyReserved4", c_float),
                ("fMyReserved5", c_float),
                ("ulMyReserved6", c_ulong),
                ("ulMyReserved7", c_ulong),
                ("ulMyReserved8", c_ulong),
                ("ulMyReserved9", c_ulong),
                ]


# noinspection PyTypeChecker
class PDPFILTERSTAT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyStatus_eMyStatus", c_uint),
                ("clMyStatus_eMyMode", c_uint),
                ("clMyStatus_eMyDynamics", c_uint),
                ("clMyStatus_uiNumPsrUsed", c_uint),
                ("clMyStatus_uiNumPhaseUsed", c_uint),
                ("clMyStatus_dMySecondsContRelOp", c_double),
                ("clMyStatus_dMyEstimatedNorthing900SecStdDev", c_double),
                ("clMyStatus_dMyEstimatedEasting900SecStdDev", c_double),
                ]


# noinspection PyTypeChecker
class PDPFILTERVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class INSUPDATESTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPosType", c_uint),
                ("iMyNumPSR", c_int),
                ("iMyNumPhase", c_int),
                ("iMyNumDOP", c_int),
                ("eMyWheelStatus", c_uint),
                ("eMyHeadingUpdateStatus", c_uint),
                ("ulMyExtSolutionStatus", c_ulong),
                ("ulMyINSUpdateOptions", c_ulong),
                ("ulMyReserved1", c_ulong),
                ("ulMyReserved2", c_ulong),
                ]


# noinspection PyTypeChecker
class PDPDETECTEDDYNAMICS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDetectedDynamics", c_uint),
                ("fMyHorizontalSpeed", c_float),
                ("fMyVerticalSpeed", c_float),
                ("bMyIsCreepDetected", c_bool),
                ]


# noinspection PyTypeChecker
class DECODEDBASESTATIONREF(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMessageEnum", c_uint),
                ("acMyDiffStationID", c_char*5),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyHeight", c_double),
                ]


# noinspection PyTypeChecker
class PDPDELTAPHASEVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyVelocityStatus", c_uint),
                ("clMyCommonSolution_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSolution_fMyLatency", c_float),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_dMyZ", c_double),
                ("clMyCommonSolution_lMyRsvdFieldForVelocityLogs", c_long),
                ]


# noinspection PyTypeChecker
class PPPFASTFEEDBACK_aclMyGrossOutlierSatelliteIDs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("idMyID", satelliteid),
                ]


# noinspection PyTypeChecker
class PPPFASTFEEDBACK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDetectedDynamics", c_uint),
                ("fMyHorizontalSpeed", c_float),
                ("fMyVerticalSpeed", c_float),
                ("bMyIsCreepDetected", c_bool),
                ("aclMyGrossOutlierSatelliteIDs_arraylength", c_ulong),
                ("aclMyGrossOutlierSatelliteIDs", PPPFASTFEEDBACK_aclMyGrossOutlierSatelliteIDs*12),
                ]


# noinspection PyTypeChecker
class DECODEDDIFFERENTIALCORRECTIONS_aclMyCorrections(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySystemID", c_ulong),
                ("fMyCorrection", c_float),
                ("fMyCorrectionStdDev", c_float),
                ("ulMyIODE", c_ulong),
                ]


# noinspection PyTypeChecker
class DECODEDDIFFERENTIALCORRECTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyType", c_uint),
                ("clMyBaseID_szMyID", c_char*4),
                ("bMyIsPartialSet", c_bool),
                ("eMySystemType", c_uint),
                ("aclMyCorrections_arraylength", c_ulong),
                ("aclMyCorrections", DECODEDDIFFERENTIALCORRECTIONS_aclMyCorrections*32),
                ]


# noinspection PyTypeChecker
class DECODEDBASESTATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMessageEnum", c_uint),
                ("acMyDiffStationID", c_char*5),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyHeight", c_double),
                ]


# noinspection PyTypeChecker
class VERIPOSPERSISTENTSTATIONS_aclMyStations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyStationID", c_ushort),
                ("usMyWeek", c_ushort),
                ("ulMyMilliseconds", c_ulong),
                ("lMyScaledXCoordinate", c_long),
                ("lMyScaledYCoordinate", c_long),
                ("lMyScaledZCoordinate", c_long),
                ]


# noinspection PyTypeChecker
class VERIPOSPERSISTENTSTATIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyStations_arraylength", c_ulong),
                ("aclMyStations", VERIPOSPERSISTENTSTATIONS_aclMyStations*120),
                ]


# noinspection PyTypeChecker
class PSRDIFFSTATIONS_clMyInfo_aclMyStations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_szMyID", c_char*4),
                ("dMyLatitudeInDegrees", c_double),
                ("dMyLongitudeInDegrees", c_double),
                ("dMyHeight", c_double),
                ("fMyDistance", c_float),
                ]


# noinspection PyTypeChecker
class PSRDIFFSTATIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_eMyType", c_uint),
                ("clMyInfo_acMyStationID", c_char*4),
                ("clMyInfo_aclMyStations_arraylength", c_ulong),
                ("clMyInfo_aclMyStations", PSRDIFFSTATIONS_clMyInfo_aclMyStations*10),
                ]


# noinspection PyTypeChecker
class VERIPOSRTCMPORTDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class ORBITANDCLOCKCORRECTIONSINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_eMySource", c_uint),
                ("clMyInfo_ulMySolutionID", c_ulong),
                ("clMyInfo_eMyRTKAssistPermission", c_uint),
                ("clMyLatestClockReferenceTime_clMyInfo_ulMyMilliseconds", c_ulong),
                ("clMyInfo_eMyPositioningPermission", c_uint),
                ]


# noinspection PyTypeChecker
class GPGNS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyStatus", c_uint),
                ]


# noinspection PyTypeChecker
class GPGNS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries_arraylength", c_ulong),
                ("clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries", GPGNS_clMySatelliteInfo_clMyCommonSolution_aclMySatelliteEntries*325),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyDOPs_fMyHDOP", c_float),
                ("eMyNMEAVersion", c_uint),
                ]


# noinspection PyTypeChecker
class SAMPLEBUFFERDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySeqNumber", c_ulong),
                ("asMyData_Len", c_ulong),
                ("asMyData", c_short*1024),
                ]


# noinspection PyTypeChecker
class HIGHRESBINDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyADC", c_ulong),
                ("ausMyBins", c_ushort*64),
                ]


# noinspection PyTypeChecker
class CORRECTIONSQUALITY_clMyCorrectionQualityEntry(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyCorrectionSource", c_uint),
                ("eMyInterfaceMode", c_uint),
                ("szMyStationID", c_char*4),
                ("fMyQuality", c_float),
                ("fMyLatency", c_float),
                ]


# noinspection PyTypeChecker
class CORRECTIONSQUALITY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCorrectionQualityEntry_arraylength", c_ulong),
                ("clMyCorrectionQualityEntry", CORRECTIONSQUALITY_clMyCorrectionQualityEntry*50),
                ]


# noinspection PyTypeChecker
class RADARSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("hulMyStatus", c_ulong),
                ("eMySolutionStatus", c_uint),
                ("eMySolutionType", c_uint),
                ("dMyHorizontalSpeedMps", c_double),
                ("dMySmoothedHorizontalSpeedMps", c_double),
                ("dMyFrequency", c_double),
                ]


# noinspection PyTypeChecker
class CANDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("bMyIsExtended", c_bool),
                ("ulMyMessageID", c_ulong),
                ("aucMyCANData", c_char*8),
                ]


# noinspection PyTypeChecker
class COARSETIMEOFFSET(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyOffset_ulMyWeeks", c_ulong),
                ("clMyOffset_ulMyMilliseconds", c_ulong),
                ("clMyOffset_bMyIsNegative", c_bool),
                ]


# noinspection PyTypeChecker
class PPPFASTIONO_aclMyDeltaPhaseIonosphereFilters(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyIonosphereRate", c_float),
                ("fMyIonosphereRateVariance", c_float),
                ("fMyObservedIonosphereRate", c_float),
                ]


# noinspection PyTypeChecker
class PPPFASTIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDeltaPhaseIonosphereFilters_arraylength", c_ulong),
                ("aclMyDeltaPhaseIonosphereFilters", PPPFASTIONO_aclMyDeltaPhaseIonosphereFilters*72),
                ]


# noinspection PyTypeChecker
class PGN129025(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ]


# noinspection PyTypeChecker
class PGN129026(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyVelocity_clMyCommonSolution_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyCommonSolution_dMyHorizontalSpeed", c_double),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class PGN129027(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class PGN129029(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyGGAQuality", c_ulong),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("bMyHasGPS", c_bool),
                ("bMyHasSBAS", c_bool),
                ("bMyHasGLONASS", c_bool),
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class PGN126992(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulUTCYear", c_ulong),
                ("ucUTCMonth", c_char),
                ("ucUTCHour", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCMinute", c_char),
                ("ulUTCMillisecond", c_ulong),
                ("UTCTimeStatus", c_uint),
                ("bMyHasGPS", c_bool),
                ("bMyHasGLONASS", c_bool),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class INSPVACMP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyWeek", c_ushort),
                ("ulMyWeekMilliseconds", c_ulong),
                ("ucMyINSStatus", c_char),
                ("ucMyGNSSPositionType", c_char),
                ("llMyLatitude", c_longlong),
                ("llMyLongitude", c_longlong),
                ("lMyHeight", c_long),
                ("sMyVelocityNorth", c_short),
                ("sMyVelocityEast", c_short),
                ("sMyVelocityUp", c_short),
                ("sMyRoll", c_short),
                ("sMyPitch", c_short),
                ("usMyAzimuth", c_ushort),
                ("sMyAzimuthRate", c_short),
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class INSPVASDCMP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyWeek", c_ushort),
                ("ulMyWeekMilliseconds", c_ulong),
                ("usMyLatitudeStdDev", c_ushort),
                ("usMyLongitudeStdDev", c_ushort),
                ("usMyHeightStdDev", c_ushort),
                ("usMyVelocityNorthStdDev", c_ushort),
                ("usMyVelocityEastStdDev", c_ushort),
                ("usMyVelocityUpStdDev", c_ushort),
                ("usMyRollStdDev", c_ushort),
                ("usMyPitchStdDev", c_ushort),
                ("usMyAzimuthStdDev", c_ushort),
                ("ucMyTimeSincePosUpdate", c_char),
                ("ucMyGNSSPositionUpdateType", c_char),
                ("ulMyExtendedSolStat", c_ulong),
                ("ucMyAlignAge", c_char),
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGPOOLSTATISTICS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clBasicProviderTransportPacketPool_ulMySize", c_ulong),
                ("clBasicProviderTransportPacketPool_ulMyHighWaterMark", c_ulong),
                ("clProviderTransportPacketPool_ulMySize", c_ulong),
                ("clProviderTransportPacketPool_ulMyHighWaterMark", c_ulong),
                ("clPolledProviderTransportPacketPool_ulMySize", c_ulong),
                ("clPolledProviderTransportPacketPool_ulMyHighWaterMark", c_ulong),
                ("clSubscriberTransportPacketPool_ulMySize", c_ulong),
                ("clSubscriberTransportPacketPool_ulMyHighWaterMark", c_ulong),
                ("clAggregatorPool_ulMySize", c_ulong),
                ("clAggregatorPool_ulMyHighWaterMark", c_ulong),
                ("clBasicSubscriberPool_ulMySize", c_ulong),
                ("clBasicSubscriberPool_ulMyHighWaterMark", c_ulong),
                ("clPeriodicSubscriberPool_ulMySize", c_ulong),
                ("clPeriodicSubscriberPool_ulMyHighWaterMark", c_ulong),
                ("clReferenceRecordPool_ulMySize", c_ulong),
                ("clReferenceRecordPool_ulMyHighWaterMark", c_ulong),
                ("clDataStoreSharedPacketPool_ulMySize", c_ulong),
                ("clDataStoreSharedPacketPool_ulMyHighWaterMark", c_ulong),
                ("clResponderRespondTransportPacketPool_ulMySize", c_ulong),
                ("clResponderRespondTransportPacketPool_ulMyHighWaterMark", c_ulong),
                ("clResponderResponseTransportPacketPool_ulMySize", c_ulong),
                ("clResponderResponseTransportPacketPool_ulMyHighWaterMark", c_ulong),
                ("clContentSubscriberTransportPacketPool_ulMySize", c_ulong),
                ("clContentSubscriberTransportPacketPool_ulMyHighWaterMark", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGEXHAUSTEDBROKERS_aclMyBrokerIds(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyPacketName", c_char*80),
                ("ulMySibling", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGEXHAUSTEDBROKERS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNumExhaustedBrokers", c_ulong),
                ("aclMyBrokerIds_arraylength", c_ulong),
                ("aclMyBrokerIds", DEBUGEXHAUSTEDBROKERS_aclMyBrokerIds*128),
                ]


# noinspection PyTypeChecker
class DEBUGPACKETPOOL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBrokerIdentfier_szMyPacketName", c_char*80),
                ("clMyBrokerIdentfier_ulMySibling", c_ulong),
                ("ulMySize", c_ulong),
                ("ulMyHighWaterMark", c_ulong),
                ("ulMyCurrentUsage", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGBROKERINFO_aclMySubscribers(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyName", c_char*32),
                ]


# noinspection PyTypeChecker
class DEBUGBROKERINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBrokerIdentifier_szMyPacketName", c_char*80),
                ("clMyBrokerIdentifier_ulMySibling", c_ulong),
                ("szMyPacketType", c_char*80),
                ("bMyIsCollection", c_bool),
                ("clMyResponder_szMyName", c_char*32),
                ("clMyProvider_szMyName", c_char*32),
                ("ulTotalNumberOfSubscribers", c_ulong),
                ("aclMySubscribers_arraylength", c_ulong),
                ("aclMySubscribers", DEBUGBROKERINFO_aclMySubscribers*64),
                ("ulAveragePublishPeriod", c_ulong),
                ("ulAcquireSequenceNumber", c_ulong),
                ("ulEmergencyPacketCount", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGPACKETUSAGE_aclMyUsers(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyName", c_char*32),
                ]


# noinspection PyTypeChecker
class DEBUGPACKETUSAGE_aclMyUsageRecords(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPacketIndex", c_ulong),
                ("ulMyUserCount", c_ulong),
                ("aclMyUsers_arraylength", c_ulong),
                ("aclMyUsers", DEBUGPACKETUSAGE_aclMyUsers*8),
                ]


# noinspection PyTypeChecker
class DEBUGPACKETUSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBrokerIdentifier_szMyPacketName", c_char*80),
                ("clMyBrokerIdentifier_ulMySibling", c_ulong),
                ("ulMyInUseCount", c_ulong),
                ("aclMyUsageRecords_arraylength", c_ulong),
                ("aclMyUsageRecords", DEBUGPACKETUSAGE_aclMyUsageRecords*32),
                ]


# noinspection PyTypeChecker
class PPPFASTSEEDPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyUndulation", c_float),
                ("clMyUserDatumPosition_clMyCommonSolution_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_fMyHgtStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("clMyCommonSolution_fMySolutionAge", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class INITIALINSSTATEINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyINSSeedValidity", c_uint),
                ("afMyAtt", c_float*3),
                ("afMyGyroBiases", c_float*3),
                ("afMyAccelBiases", c_float*3),
                ("fMyUndulation", c_float),
                ("adMyXYZ", c_double*3),
                ]


# noinspection PyTypeChecker
class J1939STATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyJ1939Node", c_uint),
                ("eMyJ1939NodeStatus", c_uint),
                ("ulMyAddressClaimCount", c_ulong),
                ("ucMyClaimedAddress", c_char),
                ]


# noinspection PyTypeChecker
class PDPLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class SATELLITEPCV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatellite_eMySystemType", c_uint),
                ("clMySatellite_idMyID", satelliteid),
                ("eMyFrequency", c_uint),
                ("afMyVariations_Len", c_ulong),
                ("afMyVariations", c_float*18),
                ]


# noinspection PyTypeChecker
class DEBUGMEMUSAGE_aclAddressSpaceMemStats(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulOSPoolSizePages", c_ulong),
                ("ulOSPoolFreePages", c_ulong),
                ("ulReserved0", c_ulong),
                ("ulReserved1", c_ulong),
                ("ulReserved2", c_ulong),
                ("ulHeapSizeBytes", c_ulong),
                ("ulTotalNumAllocations", c_ulong),
                ("ulTotalNumDeallocations", c_ulong),
                ("ulTotalBytesRequested", c_ulong),
                ("ulTotalBytesDeallocated", c_ulong),
                ("ulCurrBytesAllocated", c_ulong),
                ("ulMaxBytesAllocated", c_ulong),
                ("szAddressSpaceName", c_char*100),
                ]


# noinspection PyTypeChecker
class DEBUGMEMUSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclAddressSpaceMemStats_arraylength", c_ulong),
                ("aclAddressSpaceMemStats", DEBUGMEMUSAGE_aclAddressSpaceMemStats*16),
                ]


# noinspection PyTypeChecker
class DEBUGIDLESTATS_aclMyPerCoreIdleStats(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyCoreIndex", c_ulong),
                ("fMyIdlePercent", c_float),
                ("ulMySpare1", c_ulong),
                ("ulMySpare2", c_ulong),
                ("ulMySapre3", c_ulong),
                ("ulMySpare4", c_ulong),
                ("ulMySpare5", c_ulong),
                ("ulMySpare6", c_ulong),
                ("ulMySpare7", c_ulong),
                ("ulMySpare8", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGIDLESTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyOverallIdleStats_fMyIdlePercent", c_float),
                ("clMyOverallIdleStats_ulMySpare1", c_ulong),
                ("clMyOverallIdleStats_ulMySpare2", c_ulong),
                ("clMyOverallIdleStats_ulMySapre3", c_ulong),
                ("clMyOverallIdleStats_ulMySpare4", c_ulong),
                ("clMyOverallIdleStats_ulMySpare5", c_ulong),
                ("clMyOverallIdleStats_ulMySpare6", c_ulong),
                ("clMyOverallIdleStats_ulMySpare7", c_ulong),
                ("clMyOverallIdleStats_ulMySpare8", c_ulong),
                ("aclMyPerCoreIdleStats_arraylength", c_ulong),
                ("aclMyPerCoreIdleStats", DEBUGIDLESTATS_aclMyPerCoreIdleStats*2),
                ]


# noinspection PyTypeChecker
class DEBUGEVENTSCONFIG_aclMyCollaboratorIdentifierArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyName", c_char*32),
                ]


# noinspection PyTypeChecker
class DEBUGEVENTSCONFIG_aclMyBrokerIdentifierArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyPacketName", c_char*80),
                ("ulMySibling", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGEVENTSCONFIG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyEnabled", c_uint),
                ("eMyLoggingMode", c_uint),
                ("aeMyEventTypeArray_Len", c_ulong),
                ("aeMyEventTypeArray", c_uint*32),
                ("aclMyCollaboratorIdentifierArray_arraylength", c_ulong),
                ("aclMyCollaboratorIdentifierArray", DEBUGEVENTSCONFIG_aclMyCollaboratorIdentifierArray*32),
                ("aclMyBrokerIdentifierArray_arraylength", c_ulong),
                ("aclMyBrokerIdentifierArray", DEBUGEVENTSCONFIG_aclMyBrokerIdentifierArray*32),
                ]


# noinspection PyTypeChecker
class DEBUGPROVIDERINFO_aclMyRequestList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCollaboratorId_szMyName", c_char*32),
                ("ulMyRequestedPeriod", c_ulong),
                ("ulMyRequestedOffset", c_ulong),
                ("bMyUseMinimum", c_bool),
                ]


# noinspection PyTypeChecker
class DEBUGPROVIDERINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBrokerIdentifier_szMyPacketName", c_char*80),
                ("clMyBrokerIdentifier_ulMySibling", c_ulong),
                ("clMyProviderIdentifier_szMyName", c_char*32),
                ("ulMyProviderPeriod", c_ulong),
                ("ulMyProviderMinimumPeriod", c_ulong),
                ("ulMyActualNumRequests", c_long),
                ("aclMyRequestList_arraylength", c_ulong),
                ("aclMyRequestList", DEBUGPROVIDERINFO_aclMyRequestList*256),
                ]


# noinspection PyTypeChecker
class PGN129551(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_fMyDifferentialLag", c_float),
                ("ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class SORTEDSIGCHANMAP_aclMySigChanMaps(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("svMyChan", c_ulong),
                ("ulMyIDNumber", c_ulong),
                ("sigMyChan", c_ulong),
                ("ulMyMinosChan", c_ulong),
                ("idMySatID", satelliteid),
                ("eMySignalType", c_uint),
                ("ulMyAssignID", c_ulong),
                ("eMyChannelType", c_uint),
                ]


# noinspection PyTypeChecker
class SORTEDSIGCHANMAP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyChannelConfigurationMode", c_uint),
                ("aclMySigChanMaps_arraylength", c_ulong),
                ("aclMySigChanMaps", SORTEDSIGCHANMAP_aclMySigChanMaps*500),
                ]


# noinspection PyTypeChecker
class LBANDDECODEDFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usServiceID", c_ushort),
                ("ucSpare", c_char),
                ("aucUserData_Len", c_ulong),
                ("aucUserData", c_char*504),
                ]


# noinspection PyTypeChecker
class LBANDENCODEDFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucFrame_Len", c_ulong),
                ("aucFrame", c_char*1024),
                ]


# noinspection PyTypeChecker
class LBANDSOFTSYMFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucFrame_Len", c_ulong),
                ("aucFrame", c_char*4096),
                ]


# noinspection PyTypeChecker
class INSCONFIG_clMyINSConfigData_aclMyINSTranslations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyINSOffset", c_uint),
                ("eMyInputFrame", c_uint),
                ("afMyOffset", c_float*3),
                ("afMyOffsetStdev", c_float*3),
                ("eMySourceStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSCONFIG_clMyINSConfigData_aclMyINSRotations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyINSOffset", c_uint),
                ("eMyInputFrame", c_uint),
                ("afMyOffset", c_float*3),
                ("afMyOffsetStdev", c_float*3),
                ("eMySourceStatus", c_uint),
                ]


# noinspection PyTypeChecker
class INSCONFIG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyINSConfigData_eMyIMUType", c_uint),
                ("clMyINSConfigData_ucMyMapping", c_char),
                ("clMyINSConfigData_ucMyScaledAlignmentVel", c_char),
                ("clMyINSConfigData_usMyHeaveWindow", c_ushort),
                ("clMyINSConfigData_eMyINSProfile", c_uint),
                ("clMyINSConfigData_ulMyEnabledUpdates", c_ulong),
                ("clMyINSConfigData_eMyAlignmentMode", c_uint),
                ("clMyINSConfigData_eMyRelINSOutput", c_uint),
                ("clMyINSConfigData_bMyRelFromMaster", c_bool),
                ("clMyINSConfigData_ulMyINSRxStatus", c_ulong),
                ("clMyINSConfigData_ucMyINSSeed", c_char),
                ("clMyINSConfigData_ucMyInitialINSState", c_char),
                ("clMyINSConfigData_usMyReserved1", c_ushort),
                ("clMyINSConfigData_ulMyReserved2", c_ulong),
                ("clMyINSConfigData_ulMyReserved3", c_ulong),
                ("clMyINSConfigData_ulMyReserved4", c_ulong),
                ("clMyINSConfigData_ulMyReserved5", c_ulong),
                ("clMyINSConfigData_ulMyReserved6", c_ulong),
                ("clMyINSConfigData_ulMyReserved7", c_ulong),
                ("clMyINSConfigData_aclMyINSTranslations_arraylength", c_ulong),
                ("clMyINSConfigData_aclMyINSTranslations", INSCONFIG_clMyINSConfigData_aclMyINSTranslations*10),
                ("clMyINSConfigData_aclMyINSRotations_arraylength", c_ulong),
                ("clMyINSConfigData_aclMyINSRotations", INSCONFIG_clMyINSConfigData_aclMyINSRotations*9),
                ]


# noinspection PyTypeChecker
class SAVEDSURVEYPOSITIONS_aclMyPositions(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sMyID", c_char*5),
                ("clMyPosition_dMyLatitude", c_double),
                ("clMyPosition_dMyLongitude", c_double),
                ("clMyPosition_dMyHeight", c_double),
                ]


# noinspection PyTypeChecker
class SAVEDSURVEYPOSITIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyPositions_arraylength", c_ulong),
                ("aclMyPositions", SAVEDSURVEYPOSITIONS_aclMyPositions*32),
                ]


# noinspection PyTypeChecker
class DEBUGLARGESTMESSAGES_aclMessages(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMessageID", c_ulong),
                ("ulMaxSize", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGLARGESTMESSAGES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMessages_arraylength", c_ulong),
                ("aclMessages", DEBUGLARGESTMESSAGES_aclMessages*10),
                ]


# noinspection PyTypeChecker
class INSCALSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyINSOffset", c_uint),
                ("afMyCalibration", c_float*3),
                ("afMyCalibrationStdev", c_float*3),
                ("eMySourceStatus", c_uint),
                ("ulMyCalibrationCount", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGBOOTTIMES_aclBootTimes(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulId", c_ulong),
                ("ulTimeInMSec", c_ulong),
                ("szMeasurementName", c_char*40),
                ]


# noinspection PyTypeChecker
class DEBUGBOOTTIMES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclBootTimes_arraylength", c_ulong),
                ("aclBootTimes", DEBUGBOOTTIMES_aclBootTimes*32),
                ]


# noinspection PyTypeChecker
class ITPSDFINAL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStatusWord", c_ulong),
                ("fMyFrequencyStartMHz", c_float),
                ("fMyStepSizeHz", c_float),
                ("ausMySamples_Len", c_ulong),
                ("ausMySamples", c_ushort*1024),
                ]


# noinspection PyTypeChecker
class VERIPOSMESSAGESTATS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyMessageType", c_ulong),
                ("eMySystemType", c_uint),
                ("ulMyReceivedCount", c_ulong),
                ("ulMyLastReceivedTime", c_ulong),
                ("szMyDescription", c_char*64),
                ]


# noinspection PyTypeChecker
class VERIPOSMESSAGESTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", VERIPOSMESSAGESTATS_aclMyEntries*128),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGSUMMARY_aclMyLoggingSummaryArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyCollaboratorName", c_char*32),
                ("szMyPacketId", c_char*80),
                ("ulMySibling", c_ulong),
                ("eMyActionType", c_uint),
                ("ulMyEventCount", c_ulong),
                ("szMyContextCollaboratorName", c_char*32),
                ("szMyContextPacketId", c_char*80),
                ("ulMyContextSibling", c_ulong),
                ("eMyContextActionType", c_uint),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGSUMMARY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTotalEventsCount", c_ulong),
                ("ulMyLoggingDurationMSec", c_ulong),
                ("aclMyLoggingSummaryArray_arraylength", c_ulong),
                ("aclMyLoggingSummaryArray", DEBUGLOGGINGSUMMARY_aclMyLoggingSummaryArray*128),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGPACKETFLOW_aclMyLoggingPacketFlowArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyCollaboratorName", c_char*32),
                ("szMyPacketId", c_char*80),
                ("ulMySibling", c_ulong),
                ("ulMyEventCount", c_ulong),
                ("ulMyMinDeliveryTimeUSec", c_ulong),
                ("ulMyAvgDeliveryTimeUSec", c_ulong),
                ("ulMyMaxDeliveryTimeUSec", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGPACKETFLOW(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTotalEventsCount", c_ulong),
                ("ulMyLoggingDurationMSec", c_ulong),
                ("aclMyLoggingPacketFlowArray_arraylength", c_ulong),
                ("aclMyLoggingPacketFlowArray", DEBUGLOGGINGPACKETFLOW_aclMyLoggingPacketFlowArray*128),
                ]


# noinspection PyTypeChecker
class PFHIGHRESBINDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyEncoder", c_ulong),
                ("ausMyBins", c_ushort*64),
                ]


# noinspection PyTypeChecker
class CLOCKSTEERINGINPUT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyLastSystem", c_uint),
                ("dMyLastOffsetSeconds", c_double),
                ("dMyLastOffsetStdDevSeconds", c_double),
                ("dMyLastRateSeconds", c_double),
                ("eMyMeasurementSource", c_uint),
                ]


# noinspection PyTypeChecker
class INSOFFSETS2_aclMyLeverArm(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOffset", c_uint),
                ("eMyInputFrame", c_uint),
                ("clMyComputation_afMyElements", c_float*3),
                ("clMyComputationStdev_afMyElements", c_float*3),
                ("eMyStatus", c_uint),
                ("ulExtendedStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class INSOFFSETS2_aclMySolutionTranslation(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOffset", c_uint),
                ("eMyInputFrame", c_uint),
                ("clMyComputation_afMyElements", c_float*3),
                ("clMyComputationStdev_afMyElements", c_float*3),
                ("eMyStatus", c_uint),
                ("ulExtendedStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class INSOFFSETS2_aclMyEulerSolutionRotation(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOffset", c_uint),
                ("eMyInputFrame", c_uint),
                ("clMyComputation_afMyElements", c_float*3),
                ("clMyComputationStdev_afMyElements", c_float*3),
                ("eMyStatus", c_uint),
                ("ulExtendedStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class INSOFFSETS2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("iMyMapping", c_int),
                ("iMyGimbalMapping", c_int),
                ("bMyApplyRbvRotation", c_bool),
                ("bMyHaveDualAntenna", c_bool),
                ("bMyIsGimballed", c_bool),
                ("aclMyLeverArm_arraylength", c_ulong),
                ("aclMyLeverArm", INSOFFSETS2_aclMyLeverArm*3),
                ("aclMySolutionTranslation_arraylength", c_ulong),
                ("aclMySolutionTranslation", INSOFFSETS2_aclMySolutionTranslation*7),
                ("aclMyEulerSolutionRotation_arraylength", c_ulong),
                ("aclMyEulerSolutionRotation", INSOFFSETS2_aclMyEulerSolutionRotation*9),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGSEQUENTIAL_aclMyLoggingSequentialArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyTimeStamp", c_double),
                ("szMyCollaboratorName", c_char*32),
                ("szMyPacketId", c_char*80),
                ("ulMySibling", c_ulong),
                ("eMyEventType", c_uint),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGSEQUENTIAL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTotalEventsCount", c_ulong),
                ("ulMyLoggingDurationMSec", c_ulong),
                ("aclMyLoggingSequentialArray_arraylength", c_ulong),
                ("aclMyLoggingSequentialArray", DEBUGLOGGINGSEQUENTIAL_aclMyLoggingSequentialArray*128),
                ]


# noinspection PyTypeChecker
class PDPVELLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class ITPSDRAW(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStatusWord", c_ulong),
                ("fMyFrequencyStartMHz", c_float),
                ("fMyStepSizeHz", c_float),
                ("ausMySamples_Len", c_ulong),
                ("ausMySamples", c_ushort*1024),
                ]


# noinspection PyTypeChecker
class INSUPDATESOLUTION_clMyData_aclMyAttitudeSolution(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyAttitudeType", c_uint),
                ("bMyIsRelative", c_bool),
                ("clMyAttitude_dMyPitch", c_double),
                ("clMyAttitude_dMyRoll", c_double),
                ("clMyAttitude_dMyAzimuth", c_double),
                ]


# noinspection PyTypeChecker
class INSUPDATESOLUTION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyData_ulMyUpdateOptions", c_ulong),
                ("clMyData_ulMyUpdateType", c_ulong),
                ("clMyCommonSolution_clMyData_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_clMyData_eMyPositionType", c_uint),
                ("clMyCommonSol_LSQ_clMyData_eMyPositionStatus", c_uint),
                ("clMyCommonSol_LSQ_clMyData_eMyPositionType", c_uint),
                ("clMyCommonSol_LSQ_clMyData_eMyVelocityStatus", c_uint),
                ("clMyCommonSol_LSQ_clMyData_eMyVelocityType", c_uint),
                ("clMyVelocity_clMyCommonSol_LSQ_clMyData_dMyHorizontalSpeed", c_double),
                ("clMyDOPs_clMyData_fMyGDOP", c_float),
                ("clMyData_aclMyAttitudeSolution_arraylength", c_ulong),
                ("clMyData_aclMyAttitudeSolution", INSUPDATESOLUTION_clMyData_aclMyAttitudeSolution*2),
                ]


# noinspection PyTypeChecker
class MULTIPATHCONDITIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("dMyGeneralMultipathLevel", c_double),
                ]


# noinspection PyTypeChecker
class ITFILTCOEFTABLE_aclMyNFStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyEnabled", c_uint),
                ("eMyPFID", c_uint),
                ("eMyMode", c_uint),
                ("fMyLowerCutOffFrequency", c_float),
                ("fMyHigherCutOffFrequency", c_float),
                ("fMyFrequencyWidth", c_float),
                ("ulMyBottombit", c_ulong),
                ("alMyCoef", c_long*33),
                ]


# noinspection PyTypeChecker
class ITFILTCOEFTABLE_aclMyFilterCoefStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFrequency", c_uint),
                ("ulMyEncoderID", c_ulong),
                ("eMyDDCFilterType", c_uint),
                ("eMyClock", c_uint),
                ("fMyDDCFrequencyMHz", c_float),
                ("ulMyStatus", c_ulong),
                ("clMyBPFStatus_eMyEnabled", c_uint),
                ("clMyBPFStatus_fMyLowerCutOffFreqency", c_float),
                ("clMyBPFStatus_fMyHigherCutOffFreqency", c_float),
                ("clMyBPFStatus_ulMyBottomBit", c_ulong),
                ("clMyBPFStatus_alMyCoef", c_long*17),
                ("aclMyNFStatus_arraylength", c_ulong),
                ("aclMyNFStatus", ITFILTCOEFTABLE_aclMyNFStatus*3),
                ]


# noinspection PyTypeChecker
class ITFILTCOEFTABLE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyFilterCoefStatus_arraylength", c_ulong),
                ("aclMyFilterCoefStatus", ITFILTCOEFTABLE_aclMyFilterCoefStatus*25),
                ]


# noinspection PyTypeChecker
class ITFILTTABLE_aclMyNFStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyEnabled", c_uint),
                ("eMyPFID", c_uint),
                ("eMyMode", c_uint),
                ("fMyLowerCutOffFrequency", c_float),
                ("fMyHigherCutOffFrequency", c_float),
                ("fMyFrequencyWidth", c_float),
                ]


# noinspection PyTypeChecker
class ITFILTTABLE_aclMyFilterCoefStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFrequency", c_uint),
                ("ulMyEncoderID", c_ulong),
                ("eMyDDCFilterType", c_uint),
                ("ulMyStatus", c_ulong),
                ("clMyBPFStatus_eMyEnabled", c_uint),
                ("clMyBPFStatus_fMyLowerCutOffFreqency", c_float),
                ("clMyBPFStatus_fMyHigherCutOffFreqency", c_float),
                ("aclMyNFStatus_arraylength", c_ulong),
                ("aclMyNFStatus", ITFILTTABLE_aclMyNFStatus*3),
                ]


# noinspection PyTypeChecker
class ITFILTTABLE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyFilterCoefStatus_arraylength", c_ulong),
                ("aclMyFilterCoefStatus", ITFILTTABLE_aclMyFilterCoefStatus*25),
                ]


# noinspection PyTypeChecker
class PDPDOP2_clMyDOPs_aclMyTDOPs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("fMyDOP", c_float),
                ]


# noinspection PyTypeChecker
class PDPDOP2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyVDOP", c_float),
                ("clMyDOPs_aclMyTDOPs_arraylength", c_ulong),
                ("clMyDOPs_aclMyTDOPs", PDPDOP2_clMyDOPs_aclMyTDOPs*5),
                ]


# noinspection PyTypeChecker
class BESTFASTLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class PPPDOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyHTDOP", c_float),
                ("clMyDOPs_fMyTDOP", c_float),
                ("clMyDOPs_fMyGPSElevMask", c_float),
                ("clMyDOPs_aulMySats_Len", c_ulong),
                ("clMyDOPs_aulMySats", c_ulong*325),
                ]


# noinspection PyTypeChecker
class PDPDOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyHTDOP", c_float),
                ("clMyDOPs_fMyTDOP", c_float),
                ("clMyDOPs_fMyGPSElevMask", c_float),
                ("clMyDOPs_aulMySats_Len", c_ulong),
                ("clMyDOPs_aulMySats", c_ulong*325),
                ]


# noinspection PyTypeChecker
class DEBUGENCRYPTIONKEY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySourceId", c_ushort),
                ("eMyType", c_uint),
                ("aucMyKey_Len", c_ulong),
                ("aucMyKey", c_char*24),
                ]


# noinspection PyTypeChecker
class DEBUGDECRYPTIONKEY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMySourceId", c_ushort),
                ("eMyType", c_uint),
                ("aucMyKey_Len", c_ulong),
                ("aucMyKey", c_char*24),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGPUBLISHLATENCY_aclMyLoggingPublishLatencyArray(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyCollaboratorName", c_char*32),
                ("szMyPacketId", c_char*80),
                ("ulMySibling", c_ulong),
                ("ulMyEventCount", c_ulong),
                ("ulMyMinPublishLatencyTimeUSec", c_ulong),
                ("ulMyAvgPublishLatencyTimeUSec", c_ulong),
                ("ulMyMaxPublishLatencyTimeUSec", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGLOGGINGPUBLISHLATENCY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTotalEventsCount", c_ulong),
                ("ulMyLoggingDurationMSec", c_ulong),
                ("aclMyLoggingPublishLatencyArray_arraylength", c_ulong),
                ("aclMyLoggingPublishLatencyArray", DEBUGLOGGINGPUBLISHLATENCY_aclMyLoggingPublishLatencyArray*128),
                ]


# noinspection PyTypeChecker
class TRACKINGDOP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyHTDOP", c_float),
                ("clMyDOPs_fMyTDOP", c_float),
                ("clMyDOPs_fMyGPSElevMask", c_float),
                ("clMyDOPs_aulMySats_Len", c_ulong),
                ("clMyDOPs_aulMySats", c_ulong*325),
                ]


# noinspection PyTypeChecker
class TRACKINGDOP2_clMyDOPs_aclMyTDOPs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("fMyDOP", c_float),
                ]


# noinspection PyTypeChecker
class TRACKINGDOP2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDOPs_fMyGDOP", c_float),
                ("clMyDOPs_fMyPDOP", c_float),
                ("clMyDOPs_fMyHDOP", c_float),
                ("clMyDOPs_fMyVDOP", c_float),
                ("clMyDOPs_aclMyTDOPs_arraylength", c_ulong),
                ("clMyDOPs_aclMyTDOPs", TRACKINGDOP2_clMyDOPs_aclMyTDOPs*5),
                ]


# noinspection PyTypeChecker
class VERIPOSTRACKSTAT_aclMySignals(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignal", c_uint),
                ("fMyUserCNo", c_float),
                ]


# noinspection PyTypeChecker
class VERIPOSTRACKSTAT_aclMySatelliteEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("ulMyStatus", c_ulong),
                ("fMyAzimuthDegrees", c_float),
                ("fMyElevationDegrees", c_float),
                ("aclMySignals_arraylength", c_ulong),
                ("aclMySignals", VERIPOSTRACKSTAT_aclMySignals*5),
                ]


# noinspection PyTypeChecker
class VERIPOSTRACKSTAT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyPDOP", c_float),
                ("fMyHDOP", c_float),
                ("fMyVDOP", c_float),
                ("aclMySatelliteEntries_arraylength", c_ulong),
                ("aclMySatelliteEntries", VERIPOSTRACKSTAT_aclMySatelliteEntries*72),
                ]


# noinspection PyTypeChecker
class INHDT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ]


# noinspection PyTypeChecker
class ENCRYPTIONSTATUS_clMyEncryptionStatusEntry(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("usMyKeyID", c_ushort),
                ("idMessageID", c_ulong),
                ("eMyProtocol", c_uint),
                ("eMyEncryptionStatus", c_uint),
                ]


# noinspection PyTypeChecker
class ENCRYPTIONSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyEncryptionStatusEntry_arraylength", c_ulong),
                ("clMyEncryptionStatusEntry", ENCRYPTIONSTATUS_clMyEncryptionStatusEntry*53),
                ]


# noinspection PyTypeChecker
class DECRYPTIONSTATUS_clMyEncryptionStatusEntry(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("usMyKeyID", c_ushort),
                ("eMyProtocol", c_uint),
                ("eMyEncryptionStatus", c_uint),
                ]


# noinspection PyTypeChecker
class DECRYPTIONSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyEncryptionStatusEntry_arraylength", c_ulong),
                ("clMyEncryptionStatusEntry", DECRYPTIONSTATUS_clMyEncryptionStatusEntry*53),
                ]


# noinspection PyTypeChecker
class SRTKSUBSCRIPTIONS_aclMySubscriptions(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("usMyNetworkId", c_ushort),
                ("eMySubscriptionStatus", c_uint),
                ("eMyDecryptionStatus", c_uint),
                ("ulMyExpiryDate", c_ulong),
                ]


# noinspection PyTypeChecker
class SRTKSUBSCRIPTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySubscriptions_arraylength", c_ulong),
                ("aclMySubscriptions", SRTKSUBSCRIPTIONS_aclMySubscriptions*10),
                ]


# noinspection PyTypeChecker
class DEBUGIRQ_aclMyDebugIRQStats(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucVectorNumber", c_char),
                ("ulNumberOfTimesIRQExecutedInCore0", c_ulong),
                ("ulNumberOfTimesIRQExecutedInCore1", c_ulong),
                ("ulMyIRQTotalRunTimes", c_ulong),
                ("fMyIRQAverageRunTimes", c_float),
                ("ulMyIRQMaxRunTime", c_ulong),
                ("ulMyIRQMinRunTime", c_ulong),
                ("szVectorName", c_char*32),
                ]


# noinspection PyTypeChecker
class DEBUGIRQ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDebugIRQStats_arraylength", c_ulong),
                ("aclMyDebugIRQStats", DEBUGIRQ_aclMyDebugIRQStats*85),
                ]


# noinspection PyTypeChecker
class ITBANDPASSBANK_aclBPFBankEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFrequency", c_uint),
                ("fMyMinLowerCutOffFrequency", c_float),
                ("fMyMaxLowerCutOffFrequency", c_float),
                ("fMyMinHigherCutOffFrequency", c_float),
                ("fMyMaxHigherCutOffFrequency", c_float),
                ("fMyFrequencyStep", c_float),
                ]


# noinspection PyTypeChecker
class ITBANDPASSBANK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclBPFBankEntries_arraylength", c_ulong),
                ("aclBPFBankEntries", ITBANDPASSBANK_aclBPFBankEntries*12),
                ]


# noinspection PyTypeChecker
class ITPROGFILTBANK_aclNFParameters(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyNFMode", c_uint),
                ("fMyMinLowerCutOffFrequency", c_float),
                ("fMyMaxLowerCutOffFrequency", c_float),
                ("fMyMinHigherCutOffFrequency", c_float),
                ("fMyMaxHigherCutOffFrequency", c_float),
                ("fMyFrequencyStep", c_float),
                ("fMyNotchWidth", c_float),
                ]


# noinspection PyTypeChecker
class ITPROGFILTBANK_aclNFBankEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFrequency", c_uint),
                ("aclNFParameters_arraylength", c_ulong),
                ("aclNFParameters", ITPROGFILTBANK_aclNFParameters*5),
                ]


# noinspection PyTypeChecker
class ITPROGFILTBANK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclNFBankEntries_arraylength", c_ulong),
                ("aclNFBankEntries", ITPROGFILTBANK_aclNFBankEntries*24),
                ]


# noinspection PyTypeChecker
class DEBUGPROVIDERREQUESTS_aclMyRequestList(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCollaboratorId_szMyName", c_char*32),
                ("ulMyRequestedPeriod", c_ulong),
                ("ulMyRequestedOffset", c_ulong),
                ("bMyUseMinimum", c_bool),
                ]


# noinspection PyTypeChecker
class DEBUGPROVIDERREQUESTS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyBrokerIdentifier_szMyPacketName", c_char*80),
                ("clMyBrokerIdentifier_ulMySibling", c_ulong),
                ("clMyProviderIdentifier_szMyName", c_char*32),
                ("ulMyProviderPeriod", c_ulong),
                ("aclMyRequestList_arraylength", c_ulong),
                ("aclMyRequestList", DEBUGPROVIDERREQUESTS_aclMyRequestList*256),
                ]


# noinspection PyTypeChecker
class WEBSERVERINFO_aclWebServerProtocol(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eWebServerProtocol", c_uint),
                ("szWebServerProtocolVersion", c_char*16),
                ]


# noinspection PyTypeChecker
class WEBSERVERINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szWebServerVersion", c_char*64),
                ("ucMaxClients", c_char),
                ("ulMaxContentsSize", c_ulong),
                ("ulActualContentsSize", c_ulong),
                ("aclWebServerProtocol_arraylength", c_ulong),
                ("aclWebServerProtocol", WEBSERVERINFO_aclWebServerProtocol*4),
                ]


# noinspection PyTypeChecker
class CLIENTSESSIONINFO_aclClientSessionInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szIPADDR", c_char*48),
                ("szClientUserName", c_char*32),
                ("ulSessionDuration", c_ulong),
                ("ulSessionExpiryTime", c_ulong),
                ("ulRequestCount", c_ulong),
                ("ulInvalidRequestCount", c_ulong),
                ("ulRxByteCount", c_ulong),
                ("ulTxByteCount", c_ulong),
                ]


# noinspection PyTypeChecker
class CLIENTSESSIONINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclClientSessionInfo_arraylength", c_ulong),
                ("aclClientSessionInfo", CLIENTSESSIONINFO_aclClientSessionInfo*5),
                ]


# noinspection PyTypeChecker
class EDRDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyOffset", c_ulong),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*4096),
                ]


# noinspection PyTypeChecker
class VERIPOSBESTSOLUTION_clMySolutionBase_aclMySatellites(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("ulMySatelliteSet2", c_ulong),
                ("ulMySatelliteSet1", c_ulong),
                ]


# noinspection PyTypeChecker
class VERIPOSBESTSOLUTION_clMySolutionBase_aclMyStations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_szMyID", c_char*4),
                ]


# noinspection PyTypeChecker
class VERIPOSBESTSOLUTION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySolutionBase_eMyType", c_uint),
                ("clMySolutionBase_eMySolutionStatus", c_uint),
                ("clMyLLH_clMySolutionBase_dMyLatitude", c_double),
                ("clMyLLH_clMySolutionBase_dMyLongitude", c_double),
                ("clMyLLH_clMySolutionBase_dMyHeight", c_double),
                ("clMySolutionBase_fMyUndulation", c_float),
                ("clMyLLHStdDevs_clMySolutionBase_fMyLatStdDev", c_float),
                ("clMyLLHStdDevs_clMySolutionBase_fMyLongStdDev", c_float),
                ("clMyLLHStdDevs_clMySolutionBase_fMyHgtStdDev", c_float),
                ("clMySolutionBase_fMyEastingNorthingCovariance", c_float),
                ("clMyErrorEllipse_clMySolutionBase_fMySemiMajorAxis", c_float),
                ("clMyErrorEllipse_clMySolutionBase_fMySemiMinorAxis", c_float),
                ("clMyErrorEllipse_clMySolutionBase_fMyOrientationDegrees", c_float),
                ("clMySolutionBase_fMyHorizontalSpeedKnots", c_float),
                ("clMySolutionBase_fMyCourseOverGroundDegrees", c_float),
                ("clMySolutionBase_fMyVerticalSpeedKnots", c_float),
                ("clMySolutionBase_fMyMDE", c_float),
                ("clMySolutionBase_fMyHorizontalMDE", c_float),
                ("clMySolutionBase_fMyCorrectionLatency", c_float),
                ("clMySolutionBase_fMySolutionAge", c_float),
                ("clMyDOPs_clMySolutionBase_fMyPDOP", c_float),
                ("clMyDOPs_clMySolutionBase_fMyHDOP", c_float),
                ("clMyDOPs_clMySolutionBase_fMyVDOP", c_float),
                ("clMySolutionBase_fMyElevationMaskDegrees", c_float),
                ("clMySolutionBase_fMyHeading", c_float),
                ("clMySolutionBase_fMyHeadingStdDev", c_float),
                ("clMySolutionBase_fMyHeadingOffset", c_float),
                ("clMySolutionBase_lMyUTCOffset", c_long),
                ("clMySolutionBase_ulMyStatus", c_ulong),
                ("clMySolutionBase_aclMySatellites_arraylength", c_ulong),
                ("clMySolutionBase_aclMySatellites", VERIPOSBESTSOLUTION_clMySolutionBase_aclMySatellites*5),
                ("clMySolutionBase_aclMyStations_arraylength", c_ulong),
                ("clMySolutionBase_aclMyStations", VERIPOSBESTSOLUTION_clMySolutionBase_aclMyStations*10),
                ]


# noinspection PyTypeChecker
class VERIPOSSOLUTIONS_clMySolutionBase_aclMySatellites(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("ulMySatelliteSet2", c_ulong),
                ("ulMySatelliteSet1", c_ulong),
                ]


# noinspection PyTypeChecker
class VERIPOSSOLUTIONS_clMySolutionBase_aclMyStations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_szMyID", c_char*4),
                ]


# noinspection PyTypeChecker
class VERIPOSSOLUTIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySolutionBase_eMyType", c_uint),
                ("clMySolutionBase_eMySolutionStatus", c_uint),
                ("clMyLLH_clMySolutionBase_dMyLatitude", c_double),
                ("clMyLLH_clMySolutionBase_dMyLongitude", c_double),
                ("clMyLLH_clMySolutionBase_dMyHeight", c_double),
                ("clMySolutionBase_fMyUndulation", c_float),
                ("clMyLLHStdDevs_clMySolutionBase_fMyLatStdDev", c_float),
                ("clMyLLHStdDevs_clMySolutionBase_fMyLongStdDev", c_float),
                ("clMyLLHStdDevs_clMySolutionBase_fMyHgtStdDev", c_float),
                ("clMySolutionBase_fMyEastingNorthingCovariance", c_float),
                ("clMyErrorEllipse_clMySolutionBase_fMySemiMajorAxis", c_float),
                ("clMyErrorEllipse_clMySolutionBase_fMySemiMinorAxis", c_float),
                ("clMyErrorEllipse_clMySolutionBase_fMyOrientationDegrees", c_float),
                ("clMySolutionBase_fMyHorizontalSpeedKnots", c_float),
                ("clMySolutionBase_fMyCourseOverGroundDegrees", c_float),
                ("clMySolutionBase_fMyVerticalSpeedKnots", c_float),
                ("clMySolutionBase_fMyMDE", c_float),
                ("clMySolutionBase_fMyHorizontalMDE", c_float),
                ("clMySolutionBase_fMyCorrectionLatency", c_float),
                ("clMySolutionBase_fMySolutionAge", c_float),
                ("clMyDOPs_clMySolutionBase_fMyPDOP", c_float),
                ("clMyDOPs_clMySolutionBase_fMyHDOP", c_float),
                ("clMyDOPs_clMySolutionBase_fMyVDOP", c_float),
                ("clMySolutionBase_fMyElevationMaskDegrees", c_float),
                ("clMySolutionBase_fMyHeading", c_float),
                ("clMySolutionBase_fMyHeadingStdDev", c_float),
                ("clMySolutionBase_fMyHeadingOffset", c_float),
                ("clMySolutionBase_lMyUTCOffset", c_long),
                ("clMySolutionBase_ulMyStatus", c_ulong),
                ("clMySolutionBase_aclMySatellites_arraylength", c_ulong),
                ("clMySolutionBase_aclMySatellites", VERIPOSSOLUTIONS_clMySolutionBase_aclMySatellites*5),
                ("clMySolutionBase_aclMyStations_arraylength", c_ulong),
                ("clMySolutionBase_aclMyStations", VERIPOSSOLUTIONS_clMySolutionBase_aclMyStations*10),
                ]


# noinspection PyTypeChecker
class VERIPOSUKOOASENTENCE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMySentence", c_char*2048),
                ]


# noinspection PyTypeChecker
class TMRI(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulUTCYear", c_ulong),
                ("ucUTCMonth", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCHour", c_char),
                ("ucUTCMinute", c_char),
                ("ulUTCMillisecond", c_ulong),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyVelocity_dMyGroundTrack", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_dMyZ", c_double),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyENUBaseLine_dMyEast", c_double),
                ("clMyENUBaseLine_dMyNorthing", c_double),
                ("clMyENUBaseLine_dMyUp", c_double),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ]


# noinspection PyTypeChecker
class PSRINTEGRITYDETAIL_clMyIntegrityDetail_aclMyReliabilityValues(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyLocalTestResult", c_uint),
                ("fMyInternalReliability", c_float),
                ("fMyExternalReliabilityHorizontal", c_float),
                ("fMyExternalReliabilityVertical", c_float),
                ]


# noinspection PyTypeChecker
class PSRINTEGRITYDETAIL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyIntegrityDetail_eMyGlobalTestResult", c_uint),
                ("clMyIntegrityDetail_fMyAPosterioriVarianceFactor", c_float),
                ("clMyIntegrityDetail_fMyHPL", c_float),
                ("clMyIntegrityDetail_fMyVPL", c_float),
                ("clMyIntegrityDetail_eMyLocalTestResult", c_uint),
                ("clMyIntegrityDetail_fMyMinimumMDE", c_float),
                ("clMyIntegrityDetail_aclMyReliabilityValues_arraylength", c_ulong),
                ("clMyIntegrityDetail_aclMyReliabilityValues", PSRINTEGRITYDETAIL_clMyIntegrityDetail_aclMyReliabilityValues*72),
                ]


# noinspection PyTypeChecker
class PPPINTEGRITYDETAIL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyIntegrityDetail_eMyGlobalTestResult", c_uint),
                ("clMyIntegrityDetail_fMyAPosterioriVarianceFactor", c_float),
                ("clMyIntegrityDetail_fMyHPL", c_float),
                ("clMyIntegrityDetail_fMyVPL", c_float),
                ("clMyIntegrityDetail_eMyLocalTestResult", c_uint),
                ("clMyIntegrityDetail_fMyMinimumMDE", c_float),
                ]


# noinspection PyTypeChecker
class PPPFASTINTEGRITYDETAIL_clMyDeltaPhaseIntegrityDetail_aclMyReliabilityValues(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("eMyLocalTestResult", c_uint),
                ("fMyInternalReliability", c_float),
                ("fMyExternalReliabilityHorizontal", c_float),
                ("fMyExternalReliabilityVertical", c_float),
                ]


# noinspection PyTypeChecker
class PPPFASTINTEGRITYDETAIL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDeltaPhaseIntegrityDetail_eMyGlobalTestResult", c_uint),
                ("clMyDeltaPhaseIntegrityDetail_fMyAPosterioriVarianceFactor", c_float),
                ("clMyDeltaPhaseIntegrityDetail_fMyHPL", c_float),
                ("clMyDeltaPhaseIntegrityDetail_fMyVPL", c_float),
                ("clMyDeltaPhaseIntegrityDetail_eMyLocalTestResult", c_uint),
                ("clMyDeltaPhaseIntegrityDetail_fMyMinimumMDE", c_float),
                ("clMyDeltaPhaseIntegrityDetail_aclMyReliabilityValues_arraylength", c_ulong),
                ("clMyDeltaPhaseIntegrityDetail_aclMyReliabilityValues", PPPFASTINTEGRITYDETAIL_clMyDeltaPhaseIntegrityDetail_aclMyReliabilityValues*72),
                ]


# noinspection PyTypeChecker
class DUALANTENNAHEADING(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("fFloat", c_float),
                ("clMyHeadingInfo_fMyHeadingStdDev", c_float),
                ("clMyHeadingInfo_fMyPitchStdDev", c_float),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class DUALANTENNAHEADINGDATAREQUEST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyHeadingInterval", c_ulong),
                ]


# noinspection PyTypeChecker
class GPHDTDUALANTENNA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_bMyOutputHDT", c_bool),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMySatelliteInfo_clMyCommonSolution_ucMySystemSet", c_char),
                ]


# noinspection PyTypeChecker
class ITREFLEVEL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStatusWord", c_ulong),
                ("fMyFrequencyStartMHz", c_float),
                ("fMyStepSizeHz", c_float),
                ("ausMySamples_Len", c_ulong),
                ("ausMySamples", c_ushort*1024),
                ]


# noinspection PyTypeChecker
class WEBUICLIENTINFO_aclWebUIClientInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyClientIPAddress", c_char*48),
                ("szMyClientUserName", c_char*32),
                ("eMyClientUser", c_uint),
                ("eMyClientProtocol", c_uint),
                ("szMyDeviceType", c_char*32),
                ("szMyClientProgram", c_char*32),
                ("ulMyReserved1", c_ulong),
                ("szMyReserved2", c_char*64),
                ]


# noinspection PyTypeChecker
class WEBUICLIENTINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclWebUIClientInfo_arraylength", c_ulong),
                ("aclWebUIClientInfo", WEBUICLIENTINFO_aclWebUIClientInfo*7),
                ]


# noinspection PyTypeChecker
class RTKASSISTSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyAssistStatus_eMyState", c_uint),
                ("clMyAssistStatus_eMyStatus", c_uint),
                ("clMyAssistStatus_fMyRemainingTime", c_float),
                ("clMyAssistStatus_fMyCorrectionsAge", c_float),
                ]


# noinspection PyTypeChecker
class PPPINTERNALPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPositionStatus", c_uint),
                ("eMySolutionType", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyHeight", c_double),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyHgtStdDev", c_float),
                ("fMyDifferentialLag", c_float),
                ("clMySatelliteInfo_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_ucMyNumInSolution", c_char),
                ]


# noinspection PyTypeChecker
class RANGECMP4(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyRangeData_Len", c_ulong),
                ("aucMyRangeData", c_char*16250),
                ]


# noinspection PyTypeChecker
class INSSTDEV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyHgtStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyZStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyRollStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyPitchStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyAzimuthStdDev", c_float),
                ("clMyPVASolution_ulMyExtendedSolStat", c_ulong),
                ("clMyPVASolution_usMyTimeSincePosUpt", c_ushort),
                ("usUSHORT", c_ushort),
                ("clMyINSConfigData_ulMyEnabledUpdates", c_ulong),
                ("ulULONG", c_ulong),
                ]


# noinspection PyTypeChecker
class INSSTDEVS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_clMyPVASolution_fMyHgtStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_fMyZStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyRollStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyPitchStdDev", c_float),
                ("clMyStdDev_clMyAttitude_clMyPVASolution_fMyAzimuthStdDev", c_float),
                ("clMyPVASolution_ulMyExtendedSolStat", c_ulong),
                ("clMyPVASolution_usMyTimeSincePosUpt", c_ushort),
                ("usUSHORT", c_ushort),
                ("clMyINSConfigData_ulMyEnabledUpdates", c_ulong),
                ("ulULONG", c_ulong),
                ]


# noinspection PyTypeChecker
class RTKASSISTSTATUSDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyAssistStatus_eMyState", c_uint),
                ("clMyAssistStatus_eMyStatus", c_uint),
                ("clMyAssistStatus_fMyRemainingTime", c_float),
                ("clMyAssistStatus_fMyCorrectionsAge", c_float),
                ("clMyAssistStatus_fMyBiasStdDev", c_float),
                ]


# noinspection PyTypeChecker
class RTKMATCHEDFEEDBACK_aclMyGrossOutlierSatelliteIDs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("idMyID", satelliteid),
                ]


# noinspection PyTypeChecker
class RTKMATCHEDFEEDBACK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDetectedDynamics", c_uint),
                ("fMyHorizontalSpeed", c_float),
                ("fMyVerticalSpeed", c_float),
                ("bMyIsCreepDetected", c_bool),
                ("aclMyGrossOutlierSatelliteIDs_arraylength", c_ulong),
                ("aclMyGrossOutlierSatelliteIDs", RTKMATCHEDFEEDBACK_aclMyGrossOutlierSatelliteIDs*12),
                ]


# noinspection PyTypeChecker
class PPPCORRECTIONDRIFT_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fClockDrift", c_float),
                ("clReferenceTime_ulMyWeeks", c_ulong),
                ("clReferenceTime_ulMyMilliseconds", c_ulong),
                ]


# noinspection PyTypeChecker
class PPPCORRECTIONDRIFT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", PPPCORRECTIONDRIFT_aclMyEntries*72),
                ]


# noinspection PyTypeChecker
class SAFEMODESTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySafeModeStatus", c_uint),
                ("ulMyResetCount", c_ulong),
                ("szMyDescription", c_char*80),
                ]


# noinspection PyTypeChecker
class ITPSDDETECT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStatusWord", c_ulong),
                ("fMyFrequencyStartMHz", c_float),
                ("fMyStepSizeHz", c_float),
                ("ausMySamples_Len", c_ulong),
                ("ausMySamples", c_ushort*1024),
                ]


# noinspection PyTypeChecker
class ITDETECTSTATUS_aclMyInterferenceStatuses(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFrequency", c_uint),
                ("eMyIntDetectMethod", c_uint),
                ("fMyParameter1", c_float),
                ("fMyParameter2", c_float),
                ("fMyParameter3", c_float),
                ("fMyParameter4", c_float),
                ("ulMyReserved", c_ulong),
                ("ulMyReserved2", c_ulong),
                ("ulMyReserved3", c_ulong),
                ]


# noinspection PyTypeChecker
class ITDETECTSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyInterferenceStatuses_arraylength", c_ulong),
                ("aclMyInterferenceStatuses", ITDETECTSTATUS_aclMyInterferenceStatuses*80),
                ]


# noinspection PyTypeChecker
class LBANDRAWFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyBeamName", c_char*8),
                ("usMyServiceID", c_ushort),
                ("aucMyRawData_Len", c_ulong),
                ("aucMyRawData", c_char*64),
                ]


# noinspection PyTypeChecker
class TERRASTARBEAMSTATUS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyBeamName", c_char*8),
                ("eMySyncState", c_uint),
                ]


# noinspection PyTypeChecker
class TERRASTARBEAMSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", TERRASTARBEAMSTATUS_aclMyEntries*8),
                ]


# noinspection PyTypeChecker
class VERIPOSDECODERSTATUS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyBeamName", c_char*8),
                ("eMySyncState", c_uint),
                ("sigMyChannel", c_ulong),
                ("eMyComPort", c_uint),
                ("usMyDecoderSyncStatus", c_ushort),
                ("usMyDecoderChannel", c_ushort),
                ]


# noinspection PyTypeChecker
class VERIPOSDECODERSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", VERIPOSDECODERSTATUS_aclMyEntries*8),
                ]


# noinspection PyTypeChecker
class VERIPOSPORTDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyComPort", c_uint),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class ALIGNCORRDIAG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("pszMyMasterStationID", c_char*5),
                ("dMyMasterLatitude", c_double),
                ("dMyMasterLongitude", c_double),
                ("dMyMasterHeight", c_double),
                ("ucMyCorrectionFormat", c_char),
                ("ucMyMasterHealth", c_char),
                ("iMyDiffSourceAge", c_int),
                ("ucMyTotalUseableSats", c_char),
                ("aucMySysFreqPairs_Len", c_ulong),
                ("aucMySysFreqPairs", c_char*48),
                ]


# noinspection PyTypeChecker
class RTKCORRDIAG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("pszMyRefStationID", c_char*5),
                ("dMyLatitude", c_double),
                ("dMyLongitude", c_double),
                ("dMyHeight", c_double),
                ("ucMyCorrectionFormat", c_char),
                ("ucMyBaseHealth", c_char),
                ("iMyDiffSourceAge", c_int),
                ("ucMyPercentVisibleSatellites", c_char),
                ("aucMySysFreqData_Len", c_ulong),
                ("aucMySysFreqData", c_char*48),
                ]


# noinspection PyTypeChecker
class TRACKDIAG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyDataBytes_Len", c_ulong),
                ("aucMyDataBytes", c_char*2000),
                ]


# noinspection PyTypeChecker
class PDPDIAG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTimeTilGlideInSeconds", c_ulong),
                ("ucMyPercentSBASCorrections", c_char),
                ("ucMyPercentSBASGrid", c_char),
                ("ucMyTimeSincePDPReset", c_char),
                ("ucMyPDPResetReason", c_char),
                ("ucMyWaitingForPSRPos", c_char),
                ("ucMyGlideIsActive", c_char),
                ]


# noinspection PyTypeChecker
class VERIPOSDECODEREVENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChannel", c_ulong),
                ("eMyEvent", c_uint),
                ]


# noinspection PyTypeChecker
class FRONTENDGAIN_aclMyFrontEndGains(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyRFFrequency", c_uint),
                ("eMyRinosMode", c_uint),
                ("ulMyPulseWidth", c_ulong),
                ("fMyRawGain", c_float),
                ("fMyCalibratedGain", c_float),
                ]


# noinspection PyTypeChecker
class FRONTENDGAIN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyTemperature", c_float),
                ("aclMyFrontEndGains_arraylength", c_ulong),
                ("aclMyFrontEndGains", FRONTENDGAIN_aclMyFrontEndGains*5),
                ]


# noinspection PyTypeChecker
class VERIPOSRTCMDATAEXT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStream", c_ulong),
                ("ulMyChannel", c_ulong),
                ("ulMyMessageType", c_ulong),
                ("ulMyStationID", c_ulong),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class VERIPOSSTATIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aulMyStationIDs_Len", c_ulong),
                ("aulMyStationIDs", c_ulong*100),
                ]


# noinspection PyTypeChecker
class RTCM1019ASYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGPSEphemerides_MessageNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSatelliteID", c_char),
                ("clMyGPSEphemerides_GPSWeekNumber", c_ushort),
                ("clMyGPSEphemerides_GPSSVAccuracy", c_char),
                ("clMyGPSEphemerides_GPSCodeOnL2", c_char),
                ("clMyGPSEphemerides_GPSIDOT", c_short),
                ("clMyGPSEphemerides_GPSIODE", c_char),
                ("clMyGPSEphemerides_GPSToc", c_ushort),
                ("clMyGPSEphemerides_GPSAf2", c_char),
                ("clMyGPSEphemerides_GPSAf1", c_short),
                ("clMyGPSEphemerides_GPSAf0", c_long),
                ("clMyGPSEphemerides_GPSIODC", c_ushort),
                ("clMyGPSEphemerides_GPSCrs", c_short),
                ("clMyGPSEphemerides_GPSDeltaN", c_short),
                ("clMyGPSEphemerides_GPSM0", c_long),
                ("clMyGPSEphemerides_GPSCuc", c_short),
                ("clMyGPSEphemerides_GPSEcc", c_ulong),
                ("clMyGPSEphemerides_GPSCus", c_short),
                ("clMyGPSEphemerides_GPSSqrRootA", c_ulong),
                ("clMyGPSEphemerides_GPSToe", c_ushort),
                ("clMyGPSEphemerides_GPSCic", c_short),
                ("clMyGPSEphemerides_GPSOmega0", c_long),
                ("clMyGPSEphemerides_GPSCis", c_short),
                ("clMyGPSEphemerides_GPSI0", c_long),
                ("clMyGPSEphemerides_GPSCrc", c_short),
                ("clMyGPSEphemerides_GPSOmega", c_long),
                ("clMyGPSEphemerides_GPSOmegaDot", c_long),
                ("clMyGPSEphemerides_GPSTgd", c_char),
                ("clMyGPSEphemerides_GPSSVHealth", c_char),
                ("clMyGPSEphemerides_GPSL2PDataFlag", c_char),
                ("clMyGPSEphemerides_GPSFitInterval", c_char),
                ]


# noinspection PyTypeChecker
class RTCM1020ASYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyGLOEphem_MessageNumber", c_ushort),
                ("clMyGLOEphem_GLOSatelliteID", c_char),
                ("clMyGLOEphem_GLOSatelliteFreqChanNumber", c_char),
                ("clMyGLOEphem_GLOAlmanacHealth", c_char),
                ("clMyGLOEphem_GLOAlmanacHealthAvailability", c_char),
                ("clMyGLOEphem_GLOP1", c_char),
                ("clMyGLOEphem_GLOTk", c_ushort),
                ("clMyGLOEphem_GLOMSBBn", c_char),
                ("clMyGLOEphem_GLOP2", c_char),
                ("clMyGLOEphem_GLOTb", c_char),
                ("clMyGLOEphem_GLOXnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOXnTb", c_long),
                ("clMyGLOEphem_GLOXnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOYnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOYnTb", c_long),
                ("clMyGLOEphem_GLOYnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOZnTbFirstDerivative", c_long),
                ("clMyGLOEphem_GLOZnTb", c_long),
                ("clMyGLOEphem_GLOZnTbSecondDerivative", c_char),
                ("clMyGLOEphem_GLOP3", c_char),
                ("clMyGLOEphem_GLOGammaTb", c_short),
                ("clMyGLOEphem_GLOMP", c_char),
                ("clMyGLOEphem_GLOMlnThirdString", c_char),
                ("clMyGLOEphem_GLOTauTb", c_long),
                ("clMyGLOEphem_GLOMDeltaTau", c_char),
                ("clMyGLOEphem_GLOEn", c_char),
                ("clMyGLOEphem_GLOMP4", c_char),
                ("clMyGLOEphem_GLOMFt", c_char),
                ("clMyGLOEphem_GLOMNt", c_ushort),
                ("clMyGLOEphem_GLOMM", c_char),
                ("clMyGLOEphem_GLOAvailability", c_char),
                ("clMyGLOEphem_GLONa", c_ushort),
                ("clMyGLOEphem_GLOTauC", c_long),
                ("clMyGLOEphem_GLOMN4", c_char),
                ("clMyGLOEphem_GLOMTauGPS", c_long),
                ("clMyGLOEphem_GLOMlnFifthString", c_char),
                ("clMyGLOEphem_Reserved", c_char),
                ]


# noinspection PyTypeChecker
class IPDEBUGSTATS_aclMyIpDebugStatistics(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPhysicalInterface", c_uint),
                ("aulMyStats", c_ulong*25),
                ]


# noinspection PyTypeChecker
class IPDEBUGSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyIpDebugStatistics_arraylength", c_ulong),
                ("aclMyIpDebugStatistics", IPDEBUGSTATS_aclMyIpDebugStatistics*24),
                ]


# noinspection PyTypeChecker
class WIFIAPSETTINGS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMySSID", c_char*33),
                ("szMyPasskey", c_char*65),
                ("eMyBand", c_uint),
                ("eMySecurityType", c_uint),
                ("eMyEncryption", c_uint),
                ("eMyRegion", c_uint),
                ("iMyChannel", c_int),
                ("szMyBSSID", c_char*17),
                ]


# noinspection PyTypeChecker
class WIFIAPDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMySSID", c_char*33),
                ("szMyPasskey", c_char*65),
                ("eMyBand", c_uint),
                ("eMySecurityType", c_uint),
                ("eMyEncryption", c_uint),
                ("eMyRegion", c_uint),
                ("iMyChannel", c_int),
                ("szMyBSSID", c_char*17),
                ("szMyIPAddress", c_char*16),
                ("szMyNetMask", c_char*16),
                ("iMyMaxClients", c_int),
                ("iMyBeaconIntervalMs", c_int),
                ("iMyDTIMPeriod", c_int),
                ("eMyKeepAlive", c_uint),
                ("iMyKeepAlivePeriodMs", c_int),
                ]


# noinspection PyTypeChecker
class PPPFILTERINTEGRITYDETAIL(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyIntegrityDetail_eMyGlobalTestResult", c_uint),
                ("clMyIntegrityDetail_fMyAPosterioriVarianceFactor", c_float),
                ("clMyIntegrityDetail_fMyHPL", c_float),
                ("clMyIntegrityDetail_fMyVPL", c_float),
                ("clMyIntegrityDetail_eMyLocalTestResult", c_uint),
                ("clMyIntegrityDetail_fMyMinimumMDE", c_float),
                ]


# noinspection PyTypeChecker
class ITPSDCALIBRATIONDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("lMyVersion", c_long),
                ("eMyLNAStatus", c_uint),
                ("eMyAttenuation", c_uint),
                ("eMyRinosMode", c_uint),
                ("ulMyStatusWord", c_ulong),
                ("fMyFrequencyStartMHz", c_float),
                ("fMyStepSizeHz", c_float),
                ("fMyMiddleScaledPSDSample", c_float),
                ("fMyMeasuredPowerdBm", c_float),
                ("fMyPowerBandwidthMHz", c_float),
                ("ulMyAGCPulseWidth", c_ulong),
                ("fMyTemperature", c_float),
                ("fMyRawGain", c_float),
                ("afMySamples_Len", c_ulong),
                ("afMySamples", c_float*512),
                ]


# noinspection PyTypeChecker
class FILELIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMassStorageDevice", c_uint),
                ("eMyEntryType", c_uint),
                ("ulMyFileSize", c_ulong),
                ("ulMyLastChangeDate", c_ulong),
                ("ulMyLastChangeTime", c_ulong),
                ("aucMyFileName", c_char*128),
                ]


# noinspection PyTypeChecker
class FILETRANSFERSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eFileTransferStatus", c_uint),
                ("ulTotalTransferred", c_ulong),
                ("ulTotalTransferSize", c_ulong),
                ("szFileName", c_char*128),
                ("szErrorMsg", c_char*256),
                ]


# noinspection PyTypeChecker
class FILESYSTEMSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFileSystemStatus_eMyMassStorageDevice", c_uint),
                ("clMyFileSystemStatus_eMyFileSystemStatus", c_uint),
                ("clMyFileSystemStatus_ulMyMediaCapacity", c_ulong),
                ("clMyFileSystemStatus_szMyErrorMessage", c_char*64),
                ]


# noinspection PyTypeChecker
class NAVICRAWSUBFRAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMySatId", c_ulong),
                ("ulMyFrameId", c_ulong),
                ("aucMyRawSubframeData", c_char*33),
                ]


# noinspection PyTypeChecker
class ITFRONTENDDATA_aclMyFrontEndData(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyRFInputFrequency", c_uint),
                ("eMyLNAOnOff", c_uint),
                ("ulMyRFAttenuation", c_ulong),
                ("eMyRFGainMode", c_uint),
                ("ulMyModulus", c_ulong),
                ("ulMyPulseWidth", c_ulong),
                ("ulMyStatus", c_ulong),
                ("eMyAGCInOutRangeStatus", c_uint),
                ("ulMyADCBottomBit", c_ulong),
                ("ulMyRFLevel", c_ulong),
                ("ulMyIFLevel", c_ulong),
                ("fMyDCOffset", c_float),
                ("fMyPDFError", c_float),
                ("fMyAGCTarget", c_float),
                ("ulMyHighResBinBottomBit", c_ulong),
                ("afMyPDF", c_float*64),
                ]


# noinspection PyTypeChecker
class ITFRONTENDDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyFrontEndData_arraylength", c_ulong),
                ("aclMyFrontEndData", ITFRONTENDDATA_aclMyFrontEndData*8),
                ]


# noinspection PyTypeChecker
class WIFIACCESSPOINTSTATUS_aclMyClients(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMacAddress", c_char*17),
                ]


# noinspection PyTypeChecker
class WIFIACCESSPOINTSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("aclMyClients_arraylength", c_ulong),
                ("aclMyClients", WIFIACCESSPOINTSTATUS_aclMyClients*4),
                ]


# noinspection PyTypeChecker
class SIGDETDEBUGBUFFER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("asMyDebugBufferData_Len", c_ulong),
                ("asMyDebugBufferData", c_short*2048),
                ]


# noinspection PyTypeChecker
class SIGDETDEBUGACQ(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("dMyDoppler", c_double),
                ("dMyCodePhase", c_double),
                ("bMyPRNFound", c_bool),
                ]


# noinspection PyTypeChecker
class TRANSFERPORTSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyUSBDetectionType", c_uint),
                ("eMyUSBMode", c_uint),
                ]


# noinspection PyTypeChecker
class INSATTQS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyAttitude_clMyPVASolution_adMyQuaternion", c_double*4),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ]


# noinspection PyTypeChecker
class NAVICALMANAC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWNa", c_ulong),
                ("dMyEcc", c_double),
                ("ulMyTOA", c_ulong),
                ("dMyDi", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyRootA", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmega", c_double),
                ("dMyM0", c_double),
                ("dMyAf0", c_double),
                ("dMyAf1", c_double),
                ("ulMyAlmSVID", c_ulong),
                ("ulMyInterSigCorr", c_ulong),
                ("ulMySpare", c_ulong),
                ("ulMySVID", c_ulong),
                ]


# noinspection PyTypeChecker
class NAVICEPHEMERIS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatId", c_ulong),
                ("ulMyWN", c_ulong),
                ("dMyAf0", c_double),
                ("dMyAf1", c_double),
                ("dMyAf2", c_double),
                ("ulMyURA", c_ulong),
                ("ulMyTOC", c_ulong),
                ("dMyTGD", c_double),
                ("dMyDeltaN", c_double),
                ("ulMyIODEC", c_ulong),
                ("ulMyReserved", c_ulong),
                ("ulMyL5Health", c_ulong),
                ("ulMySHealth", c_ulong),
                ("dMyCuc", c_double),
                ("dMyCus", c_double),
                ("dMyCic", c_double),
                ("dMyCis", c_double),
                ("dMyCrc", c_double),
                ("dMyCrs", c_double),
                ("dMyIDot", c_double),
                ("ulMySpare1", c_ulong),
                ("dMyM0", c_double),
                ("ulMyTOE", c_ulong),
                ("dMyEcc", c_double),
                ("dMyRootA", c_double),
                ("dMyOmega0", c_double),
                ("dMyOmega", c_double),
                ("dMyOmegaDot", c_double),
                ("dMyI0", c_double),
                ("ulMySpare2", c_ulong),
                ("ulMyAlertFlag", c_ulong),
                ("ulMyAutoNavFlag", c_ulong),
                ]


# noinspection PyTypeChecker
class NAVICIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRNID", c_ulong),
                ("dMyAlpha0", c_double),
                ("dMyAlpha1", c_double),
                ("dMyAlpha2", c_double),
                ("dMyAlpha3", c_double),
                ("dMyBeta0", c_double),
                ("dMyBeta1", c_double),
                ("dMyBeta2", c_double),
                ("dMyBeta3", c_double),
                ("ulMySpare", c_ulong),
                ]


# noinspection PyTypeChecker
class NAVICSYSCLOCK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRNID", c_ulong),
                ("dMyA0UTC", c_double),
                ("dMyA1UTC", c_double),
                ("dMyA2UTC", c_double),
                ("lMyDeltaTls", c_long),
                ("ulMytoutc", c_ulong),
                ("ulMyWNoutc", c_ulong),
                ("ulMyWNLSF", c_ulong),
                ("ulMyDN", c_ulong),
                ("lMyDeltaTlsf", c_long),
                ("ulMyGNSSID", c_ulong),
                ("dMyA0", c_double),
                ("dMyA1", c_double),
                ("dMyA2", c_double),
                ("ulMytot", c_ulong),
                ("ulMyWNot", c_ulong),
                ("ulMySpare", c_ulong),
                ]


# noinspection PyTypeChecker
class FILESTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMediaType", c_uint),
                ("eMyFileStatus", c_uint),
                ("szMyFileName", c_char*128),
                ("ulMyFileSize", c_ulong),
                ("ulMyMediaRemainingCapacity", c_ulong),
                ("ulMyMediaTotalCapacity", c_ulong),
                ("szMyErrorMsgString", c_char*128),
                ]


# noinspection PyTypeChecker
class INSSEEDSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyINSSeedStatus", c_uint),
                ("eMyINSSeedValidity", c_uint),
                ("afMyAtt", c_float*3),
                ("adMyXYZ", c_double*3),
                ("fMyUndulation", c_float),
                ("ulMyReserved1", c_ulong),
                ("ulMyReserved2", c_ulong),
                ("ulMyReserved3", c_ulong),
                ("ulMyReserved4", c_ulong),
                ]


# noinspection PyTypeChecker
class DUALANTENNAHEADING2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyHeadingInfo_fMyBLength", c_float),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("fFloat", c_float),
                ("clMyHeadingInfo_fMyHeadingStdDev", c_float),
                ("clMyHeadingInfo_fMyPitchStdDev", c_float),
                ("acMyRoverID", c_char*4),
                ("clMyCommonSolution_acMyBaseID", c_char*4),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumTracked", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionSingleFreq", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolutionDualFreq", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus2", c_char),
                ("clMyCommonSolution_ucMyExtendedSolutionStatus", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGALandBDSSignals", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyGPSandGLOSignals", c_char),
                ]


# noinspection PyTypeChecker
class MATCHEDXYZCOV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyXYZ_clMyPosition_clMyCommonSolution_fMyCxx", c_float),
                ("clMyXYZ_clMyPosition_clMyCommonSolution_fMyCxy", c_float),
                ("clMyXYZ_clMyPosition_clMyCommonSolution_fMyCxz", c_float),
                ("clMyXYZ_clMyPosition_clMyCommonSolution_fMyCyy", c_float),
                ("clMyXYZ_clMyPosition_clMyCommonSolution_fMyCyz", c_float),
                ("clMyXYZ_clMyPosition_clMyCommonSolution_fMyCzz", c_float),
                ]


# noinspection PyTypeChecker
class DEBUGMINPERFORMANCEDATA_aclMyPerformanceStats(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyTaskID", c_ulong),
                ("fMyRunTimePercent", c_float),
                ("ulMyHeapUsed", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGMINPERFORMANCEDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyPerformanceStats_arraylength", c_ulong),
                ("aclMyPerformanceStats", DEBUGMINPERFORMANCEDATA_aclMyPerformanceStats*32),
                ]


# noinspection PyTypeChecker
class FILESYSTEMCAPACITY_aclMyFileSystems(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFileSystemType", c_uint),
                ("ullMyCapacity", c_ulonglong),
                ("ullMyUsedCapacity", c_ulonglong),
                ]


# noinspection PyTypeChecker
class FILESYSTEMCAPACITY(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyFileSystems_arraylength", c_ulong),
                ("aclMyFileSystems", FILESYSTEMCAPACITY_aclMyFileSystems*3),
                ]


# noinspection PyTypeChecker
class ITDETECTDEBUG_aclMyDetectStatusEntry(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyRFInputFreq", c_uint),
                ("eMyEnable", c_uint),
                ("fMyDetectionThresholddB", c_float),
                ("fMySampleBufferRateS", c_float),
                ("ulMyTimeWindowS", c_ulong),
                ("eMyFFTSize", c_uint),
                ("ulMyIntegrationSize", c_ulong),
                ("fMyRBWMhz", c_float),
                ("ulMyClusterSize", c_ulong),
                ("ulMyDetectionMapCount", c_ulong),
                ("ulMyDetectionMapResetCount", c_ulong),
                ("fMyCurrentCalibratedRFGaindB", c_float),
                ("fMyUsedCalibratedRFGaindB", c_float),
                ("fMyCalibratedAntennaGaindB", c_float),
                ("fMyInstantAntennaGain", c_float),
                ("fMyKurtosisValue", c_float),
                ("fMyCompressionPointdBm", c_float),
                ("fMyInstantAvgMinusMedian", c_float),
                ("fMyInstantDiffdB", c_float),
                ("fMyTotalChannelPowerdBm", c_float),
                ("fMyTotalInBandPowerdBm", c_float),
                ("ulMyStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class ITDETECTDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDetectStatusEntry_arraylength", c_ulong),
                ("aclMyDetectStatusEntry", ITDETECTDEBUG_aclMyDetectStatusEntry*8),
                ]


# noinspection PyTypeChecker
class ITRAWSAMPLES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySampleBufferMode", c_uint),
                ("ulMySourceNumber", c_ulong),
                ("fMySampleRate", c_float),
                ("fMyRFGaindB", c_float),
                ("dMyMean", c_double),
                ("dMyStd", c_double),
                ("asMySampleBufferData_Len", c_ulong),
                ("asMySampleBufferData", c_short*2048),
                ]


# noinspection PyTypeChecker
class DEBUGRANGEINFO_aclRangeInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPRN", c_ulong),
                ("fMyCodePhase", c_float),
                ("dMyCarrierPhase", c_double),
                ("fMyDoppler", c_float),
                ("ulMySignalType", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGRANGEINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclRangeInfo_arraylength", c_ulong),
                ("aclRangeInfo", DEBUGRANGEINFO_aclRangeInfo*325),
                ]


# noinspection PyTypeChecker
class SIMULATEDSATELLITESMAPPING_aclMySimulatedSatellites(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("idMySimulatedID", satelliteid),
                ("idMySourceID", satelliteid),
                ]


# noinspection PyTypeChecker
class SIMULATEDSATELLITESMAPPING(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySimulatedSatellites_arraylength", c_ulong),
                ("aclMySimulatedSatellites", SIMULATEDSATELLITESMAPPING_aclMySimulatedSatellites*72),
                ]


# noinspection PyTypeChecker
class LUAFILESYSTEMSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFileSystemStatus", c_uint),
                ("szMyError", c_char*52),
                ]


# noinspection PyTypeChecker
class LUAFILELIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyFileSize", c_ulong),
                ("ulMyLastChangedDate", c_ulong),
                ("ulMyLastChangedTime", c_ulong),
                ("szMyFilePath", c_char*256),
                ]


# noinspection PyTypeChecker
class LUASTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyExecutorNumber", c_ulong),
                ("szMyScriptCommandLine", c_char*400),
                ("szMyArgumentString", c_char*128),
                ("eMyLuaStatus", c_uint),
                ]


# noinspection PyTypeChecker
class SDDRDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySectorSize", c_ulong),
                ("ulMyOffset", c_ulong),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*4096),
                ]


# noinspection PyTypeChecker
class PPPAMBIGUITIES_aclMyAmbiguities(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("idMyID", satelliteid),
                ("fMyAmbiguity", c_float),
                ("fMyAmbiguityStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PPPAMBIGUITIES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignalType", c_uint),
                ("aclMyAmbiguities_arraylength", c_ulong),
                ("aclMyAmbiguities", PPPAMBIGUITIES_aclMyAmbiguities*22),
                ]


# noinspection PyTypeChecker
class KSXT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulUTCYear", c_ulong),
                ("ucUTCMonth", c_char),
                ("ucUTCDay", c_char),
                ("ucUTCHour", c_char),
                ("ucUTCMinute", c_char),
                ("ulUTCMillisecond", c_ulong),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyUserDatumPosition_clMyCommonSolution_dMyHeight", c_double),
                ("clMyHeadingInfo_fMyHeading", c_float),
                ("clMyHeadingInfo_fMyPitch", c_float),
                ("clMyVelocity_dMyGroundTrack", c_double),
                ("clMyVelocity_dMyHorizontalSpeed", c_double),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMyCommonSolution_eMyPositionStatus", c_uint),
                ("clMyCommonSolution_eMyPositionType", c_uint),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMySatelliteInfo_clMyCommonSolution_ucMyNumInSolution", c_char),
                ("clMyENUBaseLine_dMyEast", c_double),
                ("clMyENUBaseLine_dMyNorthing", c_double),
                ("clMyENUBaseLine_dMyUp", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_dMyZ", c_double),
                ]


# noinspection PyTypeChecker
class OCEANIXINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyPAC", c_char*16),
                ("clMyOceanixServiceInfo_eMyOperatingMode", c_uint),
                ("clMyOceanixServiceInfo_ulMySubscriptionDetails", c_ulong),
                ("clMyOceanixServiceInfo_ulMyContractEndDayOfYear", c_ulong),
                ("clMyOceanixServiceInfo_ulMyContractEndYear", c_ulong),
                ("clMyOceanixServiceInfo_ulMyTimedEnablePeriod", c_ulong),
                ("clMyOceanixServiceInfo_eMyRegionRestriction", c_uint),
                ]


# noinspection PyTypeChecker
class OCEANIXSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyAccessStatus", c_uint),
                ("eMyDecoderSyncState", c_uint),
                ("eMyRegionRestrictionStatus", c_uint),
                ]


# noinspection PyTypeChecker
class VERIPOSSTATUSDEBUG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDecoderSyncState", c_uint),
                ("ulMyAccess", c_ulong),
                ("ulMyGeogatingStatus", c_ulong),
                ("ulMySpeedGateStatus", c_ulong),
                ("ulMyDataQuality", c_ulong),
                ("ulMyEvents", c_ulong),
                ]


# noinspection PyTypeChecker
class INSMOTIONDETECT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyDynamics", c_uint),
                ("ulMyMotionCount", c_ulong),
                ("ulMyDetectionCount", c_ulong),
                ("ulMyMissedZUPTCount", c_ulong),
                ("dMySysSpeed", c_double),
                ("dMyFyAccum", c_double),
                ]


# noinspection PyTypeChecker
class RTCM1042ASYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class RTCM1042(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class RTCM1045ASYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class RTCM1045(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class RTCM1046ASYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class RTCM1046(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class RTCM1044ASYNC(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class RTCM1044(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class PPPSTATESPACEDATA_aclMyBiases(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignal", c_uint),
                ("ulMyFlags", c_ulong),
                ("ulMyCodeBiasTimeMilliseconds", c_ulong),
                ("fMyCodeBias", c_float),
                ("fMyCodeBiasStdDev", c_float),
                ("ulMyPhaseBiasTimeMilliseconds", c_ulong),
                ("fMyPhaseBias", c_float),
                ("fMyPhaseBiasStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PPPSTATESPACEDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatelliteID_eMySystemType", c_uint),
                ("clMySatelliteID_idMyID", satelliteid),
                ("bMyIsHealthy", c_bool),
                ("ulMyIOD", c_ulong),
                ("ulMyPositionReferenceTimeMilliseconds", c_ulong),
                ("clMyPosition_dMyX", c_double),
                ("clMyPosition_dMyY", c_double),
                ("clMyPosition_dMyZ", c_double),
                ("ulMyClockReferenceTimeMilliseconds", c_ulong),
                ("dMyClockBias", c_double),
                ("fMyRangeVariance", c_float),
                ("aclMyBiases_arraylength", c_ulong),
                ("aclMyBiases", PPPSTATESPACEDATA_aclMyBiases*10),
                ]


# noinspection PyTypeChecker
class ITDETECTIONMASK(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyType", c_uint),
                ("fMyFrequencyStartMHz", c_float),
                ("fMyStepSizeMHz", c_float),
                ("afMySamples_Len", c_ulong),
                ("afMySamples", c_float*64),
                ]


# noinspection PyTypeChecker
class RAWSBASFRAME2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyPrn", c_ulong),
                ("ulMySignalChannelNum", c_ulong),
                ("ucMySBASSignal", c_char),
                ("ucMyPreambleType", c_char),
                ("usMyReserve", c_ushort),
                ("ulMyWAASMsgId", c_ulong),
                ("aucMyRawFrameData", c_char*29),
                ]


# noinspection PyTypeChecker
class SATELLITEGDV(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatellite_eMySystemType", c_uint),
                ("clMySatellite_idMyID", satelliteid),
                ("eMyFrequency", c_uint),
                ("afMyVariations_Len", c_ulong),
                ("afMyVariations", c_float*18),
                ]


# noinspection PyTypeChecker
class PPPIONORESIDUALS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clSat_eMySystemType", c_uint),
                ("clSat_idMyID", satelliteid),
                ("fResidual", c_float),
                ("fElevation", c_float),
                ]


# noinspection PyTypeChecker
class PPPIONORESIDUALS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clBaseSat_eMySystemType", c_uint),
                ("clBaseSat_idMyID", satelliteid),
                ("fAverageError", c_float),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", PPPIONORESIDUALS_aclMyEntries*72),
                ]


# noinspection PyTypeChecker
class PPPIONO_aclMyIonosphereDelays(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_eMySystemType", c_uint),
                ("clMyID_idMyID", satelliteid),
                ("fMyDelay", c_float),
                ("fMyDelayStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PPPIONO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyIonosphereDelays_arraylength", c_ulong),
                ("aclMyIonosphereDelays", PPPIONO_aclMyIonosphereDelays*61),
                ]


# noinspection PyTypeChecker
class RTKMATCHEDLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*1024),
                ]


# noinspection PyTypeChecker
class ITFRONTENDCONFIGURATION_aclMyFrontEndConfiguration(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFreq", c_uint),
                ("eMySynthesizerType", c_uint),
                ("eMyRFInputFreq", c_uint),
                ("lMyFrontEndIndex", c_long),
                ("fMyLOMHz", c_float),
                ("ulMyADCNumber", c_ulong),
                ("fMyADCStartFreqMHz", c_float),
                ("fMyRFBandWidthMHz", c_float),
                ("fMyAnalogPassBandStartFreqMHz", c_float),
                ("fMyAnalogPassBandStopFreqMHz", c_float),
                ("lMyEncoder", c_long),
                ("ulMyEncoderSpeedMHz", c_ulong),
                ("fMyEncoderDDCFreqMHz", c_float),
                ("fMyEncoderCenterFreqMHz", c_float),
                ("fMyNominalDopplerMHz", c_float),
                ]


# noinspection PyTypeChecker
class ITFRONTENDCONFIGURATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyFrontEndConfiguration_arraylength", c_ulong),
                ("aclMyFrontEndConfiguration", ITFRONTENDCONFIGURATION_aclMyFrontEndConfiguration*24),
                ]


# noinspection PyTypeChecker
class DEBUGTRANSACTIONLOG_aclMyTransactionLog(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyEntryNumber", c_ulong),
                ("ulMyImageOffset", c_ulong),
                ("szMySoftwareVersion", c_char*16),
                ("szMyCompileDate", c_char*16),
                ("szMyCompileTime", c_char*16),
                ("ulMyReserved1", c_ulong),
                ("ulMyStatus", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGTRANSACTIONLOG(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyTransactionLog_arraylength", c_ulong),
                ("aclMyTransactionLog", DEBUGTRANSACTIONLOG_aclMyTransactionLog*64),
                ]


# noinspection PyTypeChecker
class BASEPOS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMessageEnum", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLongitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyHeight", c_double),
                ("clMyPosition_eMyDatumType", c_uint),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyHgtStdDev", c_float),
                ("acMyDiffStationID", c_char*4),
                ]


# noinspection PyTypeChecker
class SATELSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySatelStatus", c_uint),
                ("clMySatelErrorInfo_eMySatelError", c_uint),
                ("clMySatelErrorInfo_szMyFailedCommand", c_char*48),
                ]


# noinspection PyTypeChecker
class WIFISTATUS_aclMyClients(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMacAddress", c_char*17),
                ]


# noinspection PyTypeChecker
class WIFISTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("clMyAPInfo_szMySSID", c_char*33),
                ("clMyAPInfo_iMyRSSI", c_int),
                ("clMyAPInfo_ulMyChannel", c_ulong),
                ("clMyAPInfo_szMyBSSID", c_char*17),
                ("clMyAPInfo_eMySecurity", c_uint),
                ("aclMyClients_arraylength", c_ulong),
                ("aclMyClients", WIFISTATUS_aclMyClients*4),
                ]


# noinspection PyTypeChecker
class DEBUGUSBSTATS_aclMyUSBControllerStatistics(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyControllerNumber", c_uint),
                ("eMyUDC_STATE", c_uint),
                ("eMySpeed", c_uint),
                ("ulMyNumBusResets", c_ulong),
                ("ulMyNumSuspends", c_ulong),
                ("ulMyNumResumes", c_ulong),
                ("ulMyNumPhyErrors", c_ulong),
                ("ulMyNumStormErrors", c_ulong),
                ("iMyUSBAddress", c_int),
                ]


# noinspection PyTypeChecker
class DEBUGUSBSTATS_aclMyUsbPortStatistics(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("eMyConnectionStatus", c_uint),
                ("ulMyNumRXBytes", c_ulong),
                ("ulMyNumTXBytes", c_ulong),
                ("ulMyNumTimeouts", c_ulong),
                ("ulMyNumDroppedMessages", c_ulong),
                ("ulMyNumDroppedBytesTimeout", c_ulong),
                ("ulMyNumStatusSeconds", c_ulong),
                ("ulMyNumDroppedMessagesOverflow", c_ulong),
                ("ulMyReserved1", c_ulong),
                ("ulMyReserved2", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGUSBSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyUSBControllerStatistics_arraylength", c_ulong),
                ("aclMyUSBControllerStatistics", DEBUGUSBSTATS_aclMyUSBControllerStatistics*2),
                ("aclMyUsbPortStatistics_arraylength", c_ulong),
                ("aclMyUsbPortStatistics", DEBUGUSBSTATS_aclMyUsbPortStatistics*3),
                ]


# noinspection PyTypeChecker
class QZSSL6PRNRAMCODE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("ulMyPRN", c_ulong),
                ("lMyWeek", c_long),
                ("ulMyMilliseconds", c_ulong),
                ("aucMyBuffer", c_char*1280),
                ]


# noinspection PyTypeChecker
class WIFINETLIST_aclMyNetAPInfo(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMySSID", c_char*33),
                ("iMyRSSI", c_int),
                ("ulMyChannel", c_ulong),
                ("szMyBSSID", c_char*17),
                ("eMySecurity", c_uint),
                ]


# noinspection PyTypeChecker
class WIFINETLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyNetAPInfo_arraylength", c_ulong),
                ("aclMyNetAPInfo", WIFINETLIST_aclMyNetAPInfo*20),
                ]


# noinspection PyTypeChecker
class SATEL4INFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatel4ConfigInfo_eMySatelProtocol", c_uint),
                ("clMySatel4ConfigInfo_uiMyTxFreqHz", c_uint),
                ("clMySatel4ConfigInfo_uiMyRxFreqHz", c_uint),
                ("clMySatel4ConfigInfo_uiMyChannelSpacingHz", c_uint),
                ("clMySatel4ConfigInfo_uiMyTxPower_mW", c_uint),
                ("clMySatel4ConfigInfo_bMyFECEnabled", c_bool),
                ]


# noinspection PyTypeChecker
class SATEL9INFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMySatel9ConfigInfo_eMySatel9ModemMode", c_uint),
                ("iMyLeicaChannel", c_int),
                ("iMyNovariantChannel", c_int),
                ("clMySatel9ConfigInfo_uiMyFreqKey", c_uint),
                ("clMySatel9ConfigInfo_uiMyNetworkID", c_uint),
                ("clMySatel9ConfigInfo_uiMyMinPacketSize", c_uint),
                ("clMySatel9ConfigInfo_uiMyMaxPacketSize", c_uint),
                ("clMySatel9ConfigInfo_uiMyRetryTimeout", c_uint),
                ("clMySatel9ConfigInfo_uiMySubnet", c_uint),
                ("clMySatel9ConfigInfo_bMyRepeaters", c_bool),
                ("clMySatel9ConfigInfo_uiMyMasterPacketRepeat", c_uint),
                ("clMySatel9ConfigInfo_uiMyTxPower_mW", c_uint),
                ("clMySatel9ConfigInfo_uiMyHopTableVersion", c_uint),
                ("clMySatel9ConfigInfo_acMyFreqZone", c_char*16),
                ]


# noinspection PyTypeChecker
class COARSETIMEOFFSET2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyOffset_ulMyWeeks", c_ulong),
                ("clMyOffset_ulMyMilliseconds", c_ulong),
                ("clMyOffset_bMyIsNegative", c_bool),
                ("clMySatelliteID_eMySystemType", c_uint),
                ("clMySatelliteID_idMyID", satelliteid),
                ("eMySignalType", c_uint),
                ]


# noinspection PyTypeChecker
class ALIGNCORRREQUEST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyOption", c_uint),
                ("eMyInterfaceMode", c_uint),
                ]


# noinspection PyTypeChecker
class SSRDATAINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_eMySource", c_uint),
                ("clMyInfo_ulMySolutionID", c_ulong),
                ("clMyInfo_eMyPositionOutputPermission", c_uint),
                ("clMyInfo_eMyConvergedAccuracyPermission", c_uint),
                ("clMyInfo_eMyConvergenceTimePermission", c_uint),
                ("clMyInfo_eMyRTKAssistPermission", c_uint),
                ("clMyInfo_eMyRTKAssistDurationPermission", c_uint),
                ("clMyProviderID_clMyInfo_szMyID", c_char*4),
                ]


# noinspection PyTypeChecker
class USERI2CRESPONSE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ucMySlaveDeviceAddress", c_char),
                ("ulMySlaveRegisterAddress", c_ulong),
                ("eMyStatusCode", c_uint),
                ("eMyOperationMode", c_uint),
                ("ulMyTransactionID", c_ulong),
                ("aucMyReadData_Len", c_ulong),
                ("aucMyReadData", c_char*256),
                ]


# noinspection PyTypeChecker
class GALCNAVRAWPAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("sigMyChan", c_ulong),
                ("ulMySatID", c_ulong),
                ("ulMyPageID", c_ulong),
                ("aucMyPage", c_char*58),
                ]


# noinspection PyTypeChecker
class LUAOUTPUT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySequenceNumber", c_ulong),
                ("ulMyLuaExecutor", c_ulong),
                ("eMySource", c_uint),
                ("ulMyData", c_char*128),
                ]


# noinspection PyTypeChecker
class SIMULATESATELLITEERRORSTATUS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystemType", c_uint),
                ("eMyErrorType", c_uint),
                ("aulMyParameters", c_ulong*32),
                ]


# noinspection PyTypeChecker
class SIMULATESATELLITEERRORSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyErrorConfig", c_uint),
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", SIMULATESATELLITEERRORSTATUS_aclMyEntries*16),
                ]


# noinspection PyTypeChecker
class SIMULATEDSATELLITEERRORS_aclMyEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyID_idMyID", satelliteid),
                ("clMyID_eMySystemType", c_uint),
                ("eMyErrorType", c_uint),
                ("dMyElevation", c_double),
                ("dMyAzimuth", c_double),
                ("adMyRandomErrorAmplitude", c_double*3),
                ("adMyRandomPhaseOffsetError", c_double*3),
                ("dMyECIRotationError", c_double),
                ]


# noinspection PyTypeChecker
class SIMULATEDSATELLITEERRORS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyEntries_arraylength", c_ulong),
                ("aclMyEntries", SIMULATEDSATELLITEERRORS_aclMyEntries*72),
                ]


# noinspection PyTypeChecker
class DEBUGRETRIEDBROKERS_aclMyBrokerIds(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyPacketName", c_char*80),
                ("ulMySibling", c_ulong),
                ]


# noinspection PyTypeChecker
class DEBUGRETRIEDBROKERS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyNumRetriedBrokers", c_ulong),
                ("aclMyBrokerIds_arraylength", c_ulong),
                ("aclMyBrokerIds", DEBUGRETRIEDBROKERS_aclMyBrokerIds*128),
                ]


# noinspection PyTypeChecker
class INPUTPARSERSTATUS_aclMyInputParserStatus(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPort", c_uint),
                ("ulMyInterfacemode", c_uint),
                ("eMyState", c_uint),
                ("clMyLastTime_ulMyWeeks", c_ulong),
                ("clMyLastTime_ulMyMilliseconds", c_ulong),
                ("ulMyTotalAccepted", c_ulong),
                ("ulMyTotalRejected", c_ulong),
                ("ulMyLastStateBytes", c_ulong),
                ("ulMyBaudRate", c_ulong),
                ("eMyParity", c_uint),
                ("ulMyDataBits", c_ulong),
                ("ulMyStopBits", c_ulong),
                ]


# noinspection PyTypeChecker
class INPUTPARSERSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyInputParserStatus_arraylength", c_ulong),
                ("aclMyInputParserStatus", INPUTPARSERSTATUS_aclMyInputParserStatus*53),
                ]


# noinspection PyTypeChecker
class ANNOTATIONCMP(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyMessage", c_char*2048),
                ]


# noinspection PyTypeChecker
class PPPSEEDAPPLICATIONSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_dMyHeight", c_double),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyLatStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyLongStdDev", c_float),
                ("clMyLLHStdDev_clMyLLH_clMyPosition_fMyHgtStdDev", c_float),
                ]


# noinspection PyTypeChecker
class PPPSEEDSTORESTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("fMyHorizontalStdDev", c_float),
                ]


# noinspection PyTypeChecker
class DEBUGSIGCHANASSIGN_aclMySigChanAssign(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySatelliteID", c_ulong),
                ("svMyChan", c_ulong),
                ("ulMyIDNumber", c_ulong),
                ("sigMyChan", c_ulong),
                ("ulMyMinosID", c_ulong),
                ("sigMyMasterChan", c_ulong),
                ("eMySignalType", c_uint),
                ("ulMyAssignID", c_ulong),
                ("eMyAssignType", c_uint),
                ("eMyLegacySearchSpeed", c_uint),
                ("lMyLegacyDoppler", c_long),
                ("ulMyLegacyDopplerWindow", c_ulong),
                ("lMyOriginalDoppler", c_long),
                ("ulMyOriginalDopplerWindow", c_ulong),
                ("eMyFFTSearchSpeed", c_uint),
                ("lMyFFTDoppler", c_long),
                ("ulMyFFTLowerDoppler", c_ulong),
                ("ulMyFFTUpperDoppler", c_ulong),
                ("ulMyLBandBaudRate", c_ulong),
                ("ulMyLBandFrequency", c_ulong),
                ("ulMyServiceID", c_ulong),
                ("ulMyModeWord", c_ulong),
                ("acMyLBandBeamName", c_char*8),
                ]


# noinspection PyTypeChecker
class DEBUGSIGCHANASSIGN(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMySigChanAssign_arraylength", c_ulong),
                ("aclMySigChanAssign", DEBUGSIGCHANASSIGN_aclMySigChanAssign*10),
                ]


# noinspection PyTypeChecker
class SIGNALACQSTATS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyMeasurementSource", c_uint),
                ("eMySignalType", c_uint),
                ("ulMySatID", c_ulong),
                ("sigMyChan", c_ulong),
                ("clMyAcquisitionStats_llMySkySearchInitTimeMS", c_longlong),
                ("clMyAcquisitionStats_llMySkySearchHitTimeMS", c_longlong),
                ("clMyAcquisitionStats_llMyCodeSweepTimeMS", c_longlong),
                ("clMyAcquisitionStats_llMyFrequencyPullinTimeMS", c_longlong),
                ("clMyAcquisitionStats_llMyBitSyncTimeMS", c_longlong),
                ("clMyAcquisitionStats_llMyFLLTimeMS", c_longlong),
                ("clMyAcquisitionStats_llMyTrackingTimeMS", c_longlong),
                ]


# noinspection PyTypeChecker
class TIMETOPOSITIONEVENT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("llMyMilliSecondsSinceBoot", c_longlong),
                ("eMyEvent", c_uint),
                ]


# noinspection PyTypeChecker
class QZSSCNAVRAWMESSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMyPrn", c_ulong),
                ("eMySignalType", c_uint),
                ("ulMyMessageId", c_ulong),
                ("aucMyRawFrameData", c_char*38),
                ]


# noinspection PyTypeChecker
class GPSCNAVRAWMESSAGE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySigChanNum", c_ulong),
                ("ulMyPrn", c_ulong),
                ("eMySignalType", c_uint),
                ("ulMyFrameId", c_ulong),
                ("aucMyRawFrameData", c_char*38),
                ]


# noinspection PyTypeChecker
class RANKLIST_aclMyRanks(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyRank", c_ulong),
                ("idMyID", satelliteid),
                ("svMyChan", c_ulong),
                ("eMyTrackingState", c_uint),
                ("bMyAvailable", c_bool),
                ]


# noinspection PyTypeChecker
class RANKLIST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySystem", c_uint),
                ("aclMyRanks_arraylength", c_ulong),
                ("aclMyRanks", RANKLIST_aclMyRanks*48),
                ]


# noinspection PyTypeChecker
class CORRIMUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyAccumCount", c_ulong),
                ("adMyCorr_wb_ib", c_double*3),
                ("adMyCorr_fb", c_double*3),
                ("fMyLatencyMS", c_float),
                ("ulULONG", c_ulong),
                ]


# noinspection PyTypeChecker
class PPPMANAGERSTATUS_aclMyPPPManagerStatusEntries(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMySiblingID", c_ulong),
                ("eMyMeasurementSource", c_uint),
                ("eMySSRDataSource", c_uint),
                ("eMyCoverageArea ", c_uint),
                ("ulMySolutionID", c_ulong),
                ("clMyCorrectionsIdentifier_szMyID", c_char*4),
                ]


# noinspection PyTypeChecker
class PPPMANAGERSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyPPPManagerStatusEntries_arraylength", c_ulong),
                ("aclMyPPPManagerStatusEntries", PPPMANAGERSTATUS_aclMyPPPManagerStatusEntries*3),
                ]


# noinspection PyTypeChecker
class SSRCORRECTIONSDIGEST_aclMyBiases(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignal", c_uint),
                ("ulMyFlags", c_ulong),
                ("ulMyCodeBiasTimeMilliseconds", c_ulong),
                ("fMyCodeBias", c_float),
                ("fMyCodeBiasStdDev", c_float),
                ("ulMyPhaseBiasTimeMilliseconds", c_ulong),
                ("fMyPhaseBias", c_float),
                ("fMyPhaseBiasStdDev", c_float),
                ("ulMyPhaseBiasIOD", c_ulong),
                ]


# noinspection PyTypeChecker
class SSRCORRECTIONSDIGEST(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySource", c_uint),
                ("clMyProvider_szMyID", c_char*4),
                ("ulMySolutionID", c_ulong),
                ("clMySatelliteID_eMySystemType", c_uint),
                ("clMySatelliteID_idMyID", satelliteid),
                ("ulMyIOD", c_ulong),
                ("ulMyPositionReferenceTimeMilliseconds", c_ulong),
                ("fMyXCorrection", c_float),
                ("fMyYCorrection", c_float),
                ("fMyZCorrection", c_float),
                ("fMyXCorrectionRate", c_float),
                ("fMyYCorrectionRate", c_float),
                ("fMyZCorrectionRate", c_float),
                ("ulMyClockReferenceTimeMilliseconds", c_ulong),
                ("fMyClockCorrection", c_float),
                ("fMyRangeStdDev", c_float),
                ("fMyIonoDelay", c_float),
                ("fMyIonoDelayStdDev", c_float),
                ("aclMyBiases_arraylength", c_ulong),
                ("aclMyBiases", SSRCORRECTIONSDIGEST_aclMyBiases*10),
                ]


# noinspection PyTypeChecker
class MARKDMIPVAS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyWeek", c_ulong),
                ("dMySeconds", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLatitude", c_double),
                ("clMyLLHDegreesOrtho_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyLongitude", c_double),
                ("clMyLLH_clMyLLH_clMyPosition_clMyCommonSolution_clMyPVASolution_dMyHeight", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyNEU_clMyVelocity_clMyCommonSolution_clMyPVASolution_dMyZ", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyRoll", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyPitch", c_double),
                ("clMyAttitude_clMyAttitude_clMyPVASolution_dMyAzimuth", c_double),
                ("clMyPVASolution_eMyINSStatus", c_uint),
                ("lMyMeasurement", c_long),
                ]


# noinspection PyTypeChecker
class PPPINTERNALSEED(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyCoords_clMyPosition_dMyX", c_double),
                ("clMyCoords_clMyPosition_dMyY", c_double),
                ("clMyCoords_clMyPosition_dMyZ", c_double),
                ("clMyStdDevs_clMyPosition_fMyXStdDev", c_float),
                ("clMyStdDevs_clMyPosition_fMyYStdDev", c_float),
                ("clMyStdDevs_clMyPosition_fMyZStdDev", c_float),
                ("clMyPosition_fMyCxy", c_float),
                ("clMyPosition_fMyCxz", c_float),
                ("clMyPosition_fMyCyz", c_float),
                ]


# noinspection PyTypeChecker
class SPRINKLERDATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyConfig", c_ulong),
                ("ulMyStartSampleIndex", c_ulong),
                ("asMySamples_Len", c_ulong),
                ("asMySamples", c_short*1024),
                ]


# noinspection PyTypeChecker
class SPRINKLERDATAH(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMySignal", c_uint),
                ("eMyFreqBand", c_uint),
                ("ulMyConfig", c_ulong),
                ("ulMyRFStartFrequency", c_ulong),
                ("ulMySampleRate", c_ulong),
                ("eMyCollectionStatus", c_uint),
                ("usMyADCPulseWidth", c_ushort),
                ("usMyAGCPulseModulus", c_ushort),
                ("ulMyNumSamplesCollected", c_ulong),
                ]


# noinspection PyTypeChecker
class VERIPOSREGIONALBEAM_clMyRegion_aclMyBoundaryPoints(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("fMyLatitudeInDegrees", c_float),
                ("fMyLongitudeInDegrees", c_float),
                ]


# noinspection PyTypeChecker
class VERIPOSREGIONALBEAM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyBeamID", c_ulong),
                ("clMyBeamInformation_acMyName", c_char*8),
                ("clMyBeamInformation_acMyRegionID", c_char*8),
                ("clMyBeamInformation_ulMyFrequencyInHz", c_ulong),
                ("clMyBeamInformation_ulMyBaudRate", c_ulong),
                ("clMyBeamInformation_fMyLongitude", c_float),
                ("clMyBeamInformation_ulMyBeamAccess", c_ulong),
                ("ulMySatelliteProviderID", c_ulong),
                ("clMyInteriorPoint_clMyRegion_fMyLatitudeInDegrees", c_float),
                ("clMyInteriorPoint_clMyRegion_fMyLongitudeInDegrees", c_float),
                ("clMyRegion_aclMyBoundaryPoints_arraylength", c_ulong),
                ("clMyRegion_aclMyBoundaryPoints", VERIPOSREGIONALBEAM_clMyRegion_aclMyBoundaryPoints*11),
                ]


# noinspection PyTypeChecker
class VERIPOSPERMISSIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyPositionOutputPermission", c_uint),
                ("eMyConvergedAccuracyPermission", c_uint),
                ("eMyConvergenceTimePermission", c_uint),
                ("eMyRTKAssistPermission", c_uint),
                ("eMyRTKAssistDurationPermission", c_uint),
                ]


# noinspection PyTypeChecker
class VERIPOSRTCMV3DATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyStream", c_ulong),
                ("aucMyData_Len", c_ulong),
                ("aucMyData", c_char*1024),
                ]


# noinspection PyTypeChecker
class USERANTENNA_clMyAntennaParameters_aclMyPCCs(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyFrequency", c_uint),
                ("afMyPCO", c_float*3),
                ("afMyPCV", c_float*19),
                ]


# noinspection PyTypeChecker
class USERANTENNA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyUserAntenna", c_uint),
                ("clMyAntennaParameters_acMyAntennaName", c_char*16),
                ("clMyAntennaParameters_aclMyPCCs_arraylength", c_ulong),
                ("clMyAntennaParameters_aclMyPCCs", USERANTENNA_clMyAntennaParameters_aclMyPCCs*24),
                ]


# noinspection PyTypeChecker
class MCMFSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyCurrentBootMCMFEnable", c_uint),
                ("bMyMCMFAllowedByModel", c_bool),
                ("ulMyChanConfigID", c_ulong),
                ("eMyNextBootMCMFEnable", c_uint),
                ]


# noinspection PyTypeChecker
class LBANDRAWFRAME2(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("acMyBeamName", c_char*8),
                ("usMyServiceID", c_ushort),
                ("sigMyChan", c_ulong),
                ("aucMyRawData_Len", c_ulong),
                ("aucMyRawData", c_char*64),
                ]


# noinspection PyTypeChecker
class VERIPOSTRINAVSENTENCE(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMySentence", c_char*2048),
                ]


# noinspection PyTypeChecker
class TECTONICSCOMPENSATION(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("eMyStatus", c_uint),
                ("acMyName", c_char*32),
                ("clMyECEFStationVelocity_fMyX", c_float),
                ("clMyECEFStationVelocity_fMyY", c_float),
                ("clMyECEFStationVelocity_fMyZ", c_float),
                ]


# noinspection PyTypeChecker
class SSRDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyInfo_eMySource", c_uint),
                ("clMyProviderID_clMyInfo_szMyID", c_char*4),
                ("clMyName_clMyDatumID_clMyCoordinateMetadata_clMyInfo_acMyName", c_char*32),
                ("clMyDatumID_clMyCoordinateMetadata_clMyInfo_ulMyEPSGCode", c_ulong),
                ("clMyCoordinateMetadata_clMyInfo_dMyEpoch", c_double),
                ]


# noinspection PyTypeChecker
class PPPDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_acMyName", c_char*32),
                ("clMyDatumID_clMyMetadata_ulMyEPSGCode", c_ulong),
                ("clMyMetadata_dMyEpoch", c_double),
                ("clMyMetadata_eMyTransformationStatus", c_uint),
                ]


# noinspection PyTypeChecker
class PPPFASTMETADATA(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_clMyPosition_clMyCommonSolution_acMyName", c_char*32),
                ("clMyMetadata_clMyPosition_clMyCommonSolution_dMyEpoch", c_double),
                ("clMyName_clMyDatumID_clMyMetadata_clMyUserDatumPosition_clMyCommonSolution_acMyName", c_char*32),
                ("clMyMetadata_clMyUserDatumPosition_clMyCommonSolution_dMyEpoch", c_double),
                ]


# noinspection PyTypeChecker
class GEODETICDATUMS_aclMyDatums(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyID_acMyName", c_char*32),
                ("clMyID_ulMyEPSGCode", c_ulong),
                ("eMyAnchor", c_uint),
                ("dMySemiMajorAxis", c_double),
                ("dMyInverseFlattening", c_double),
                ]


# noinspection PyTypeChecker
class GEODETICDATUMS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyDatums_arraylength", c_ulong),
                ("aclMyDatums", GEODETICDATUMS_aclMyDatums*65),
                ]


# noinspection PyTypeChecker
class DATUMTRANSFORMATIONS_aclMyTransformations(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyFromName_acMyName", c_char*32),
                ("clMyToName_acMyName", c_char*32),
                ("dMyEpoch", c_double),
                ("fMyXTranslation", c_float),
                ("fMyYTranslation", c_float),
                ("fMyZTranslation", c_float),
                ("fMyXRotation", c_float),
                ("fMyYRotation", c_float),
                ("fMyZRotation", c_float),
                ("fMyScaleDifference", c_float),
                ("fMyXTranslationRate", c_float),
                ("fMyYTranslationRate", c_float),
                ("fMyZTranslationRate", c_float),
                ("fMyXRotationRate", c_float),
                ("fMyYRotationRate", c_float),
                ("fMyZRotationRate", c_float),
                ("fMyScaleDifferenceRate", c_float),
                ]


# noinspection PyTypeChecker
class DATUMTRANSFORMATIONS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("aclMyTransformations_arraylength", c_ulong),
                ("aclMyTransformations", DATUMTRANSFORMATIONS_aclMyTransformations*64),
                ]


# noinspection PyTypeChecker
class EXPANDEDDATUM(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyDatumData_clMyDatum_eMyType", c_uint),
                ("clMyDatumData_clMyDatum_dMySemiMajorAxis", c_double),
                ("clMyDatumData_clMyDatum_dMyInverseFlattening", c_double),
                ("clMyExpansionTime_clMyDatum_dMyScale", c_double),
                ("clMyTranslation_clMyExpansionTime_clMyDatum_dMyX", c_double),
                ("clMyTranslation_clMyExpansionTime_clMyDatum_dMyY", c_double),
                ("clMyTranslation_clMyExpansionTime_clMyDatum_dMyZ", c_double),
                ("clMyRotations_clMyExpansionTime_clMyDatum_dMyX", c_double),
                ("clMyRotations_clMyExpansionTime_clMyDatum_dMyY", c_double),
                ("clMyRotations_clMyExpansionTime_clMyDatum_dMyZ", c_double),
                ]


# noinspection PyTypeChecker
class PSRDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_acMyName", c_char*32),
                ("clMyDatumID_clMyMetadata_ulMyEPSGCode", c_ulong),
                ("clMyMetadata_dMyEpoch", c_double),
                ("clMyMetadata_eMyTransformationStatus", c_uint),
                ]


# noinspection PyTypeChecker
class CAKEDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_acMyName", c_char*32),
                ("clMyDatumID_clMyMetadata_ulMyEPSGCode", c_ulong),
                ("clMyMetadata_dMyEpoch", c_double),
                ("clMyMetadata_eMyTransformationStatus", c_uint),
                ]


# noinspection PyTypeChecker
class BESTGNSSDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_acMyName", c_char*32),
                ("clMyDatumID_clMyMetadata_ulMyEPSGCode", c_ulong),
                ("clMyMetadata_dMyEpoch", c_double),
                ("clMyMetadata_eMyTransformationStatus", c_uint),
                ]


# noinspection PyTypeChecker
class PDPDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_acMyName", c_char*32),
                ("clMyDatumID_clMyMetadata_ulMyEPSGCode", c_ulong),
                ("clMyMetadata_dMyEpoch", c_double),
                ("clMyMetadata_eMyTransformationStatus", c_uint),
                ]


# noinspection PyTypeChecker
class RTKDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_acMyName", c_char*32),
                ("clMyDatumID_clMyMetadata_ulMyEPSGCode", c_ulong),
                ("clMyMetadata_dMyEpoch", c_double),
                ("clMyMetadata_eMyTransformationStatus", c_uint),
                ]


# noinspection PyTypeChecker
class BESTDATUMINFO(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyName_clMyDatumID_clMyMetadata_acMyName", c_char*32),
                ("clMyDatumID_clMyMetadata_ulMyEPSGCode", c_ulong),
                ("clMyMetadata_dMyEpoch", c_double),
                ("clMyMetadata_eMyTransformationStatus", c_uint),
                ]


# noinspection PyTypeChecker
class TILTBIASES(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyAccelBiases_dMyX", c_double),
                ("clMyAccelBiases_dMyY", c_double),
                ("clMyAccelBiases_dMyZ", c_double),
                ("clMyGyroBiases_dMyX", c_double),
                ("clMyGyroBiases_dMyY", c_double),
                ("clMyGyroBiases_dMyZ", c_double),
                ]


# noinspection PyTypeChecker
class PMDT(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("cMyOption", c_char),
                ("iMyReserved", c_int),
                ("iMyFeet", c_int),
                ("iMyInches", c_int),
                ("fMyMetres", c_float),
                ]


# noinspection PyTypeChecker
class TILTSTATUS(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("ulMyCompensationStatus", c_ulong),
                ("clMyAttitude_dMyPitch", c_double),
                ("clMyAttitude_dMyRoll", c_double),
                ("clMyPositionCorrection_dMyX", c_double),
                ("clMyPositionCorrection_dMyY", c_double),
                ("clMyPositionCorrection_dMyZ", c_double),
                ("clMyAttitude_dMyAzimuth", c_double),
                ("ulULONG", c_ulong),
                ]


# noinspection PyTypeChecker
class BLUETOOTHNAME(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("szMyDeviceName", c_char*32),
                ]


# noinspection PyTypeChecker
class INSVELUSER(Structure, BaseStructMixin):
    _pack_ = 1
    _fields_ = [
                ("clMyVelocity_clMyUserVelocity_clMyPVASolution_dMyX", c_double),
                ("clMyVelocity_clMyUserVelocity_clMyPVASolution_dMyY", c_double),
                ("clMyVelocity_clMyUserVelocity_clMyPVASolution_dMyZ", c_double),
                ("clMyStdDev_clMyUserVelocity_clMyPVASolution_fMyXStdDev", c_float),
                ("clMyStdDev_clMyUserVelocity_clMyPVASolution_fMyYStdDev", c_float),
                ("clMyStdDev_clMyUserVelocity_clMyPVASolution_fMyZStdDev", c_float),
                ("clMyPVASolution_fMySlipAngle", c_float),
                ("ulULONG", c_ulong),
                ("ulULONG", c_ulong),
                ("clMyPVASolution_usMyExtVelStatus", c_ushort),
                ]


# Remove the c_bool 4 byte patch
c_bool = temp_c_bool


mapping = {
    5: LOGLIST,
    6: RTCAOBS,
    7: GPSEPHEM,
    8: IONUTC,
    9: OBSERVATIONS,
    10: RTCA1,
    11: RTCAREF,
    16: CLOCKMODEL,
    23: DECODERCMDS,
    24: RAWNAVDATA,
    25: RAWGPSSUBFRAME,
    26: CLOCKSTEERING,
    31: GPSOL_CTS,
    32: CHANDEBUG,
    33: GPSOL_MON,
    34: GPSOL_POS,
    37: VERSION,
    39: DEBUGMEMORY,
    40: DEBUGPROCESS,
    41: RAWEPHEM,
    42: BESTPOS,
    43: RANGE,
    45: DECODERSTATUS,
    47: PSRPOS,
    48: SATVIS,
    69: BAT,
    71: PROPAGATEDCLOCKMODEL,
    72: PORTSTATS,
    73: ALMANAC,
    74: RAWALM,
    77: GPSOL_VEL,
    79: RTCAOBSIN,
    80: RTCAREFIN,
    82: GPSOL_AZEL,
    83: TRACKSTAT,
    84: SATSTAT,
    85: LOOPACCUM,
    86: LOOPGAINS,
    93: RXSTATUS,
    94: RXSTATUSEVENT,
    96: MATCHEDPOS,
    99: BESTVEL,
    100: PSRVEL,
    101: TIME,
    103: CMROBS,
    104: CMROBSIN,
    105: CMRREF,
    106: CMRREFIN,
    107: RTCM1,
    108: RTCM18OUT,
    109: RTCM19OUT,
    110: RTCM1IN,
    111: RTCM20IN,
    112: RTCM21IN,
    113: RTCM22IN,
    114: RTCM3IN,
    115: RTCM59IN,
    116: RTCM59,
    117: RTCM3,
    118: RTCM22,
    119: RTCM21OUT,
    120: RTCM20OUT,
    121: RTCM19IN,
    122: RTCM18IN,
    126: RANGEPN,
    128: RXCONFIG,
    129: RTCM16,
    130: RTCM16IN,
    132: DEBUGETHERS,
    133: DEBUGMSGQS,
    140: RANGECMP,
    141: RTKPOS,
    146: FILEDUMP,
    147: FILEHDR,
    148: GROUPDEF,
    150: METDEF,
    151: SCHDEF,
    153: SITEDEF,
    156: PROJECTDEF,
    158: FILECHANNEL,
    159: DIRENT,
    161: NAVIGATE,
    172: AVEPOS,
    174: PSRDOP,
    175: REFSTATION,
    176: EXTVERSION,
    181: MARKPOS,
    187: CURRENTSET,
    188: PDCSTATUS,
    191: HIGHRATEL1DATA,
    193: DEBUGPROCESSIDLES,
    194: DEBUGPROCESSNAMES,
    195: RXHWLEVELS,
    196: RTCAIN,
    198: NVMSTATS,
    199: CTRLSUM,
    206: VALIDMODELS,
    207: SAVEDERROR,
    209: AUDIODEF,
    210: HWLEVELS,
    215: RTKDATA,
    216: RTKVEL,
    217: GPALM,
    218: GPGGA,
    219: GPGLL,
    220: GPGRS,
    221: GPGSA,
    222: GPGST,
    223: GPGSV,
    224: GPRMB,
    225: GPRMC,
    226: GPVTG,
    227: GPZDA,
    231: MARKTIME,
    239: SLEEPMODE,
    241: BESTXYZ,
    242: MATCHEDXYZ,
    243: PSRXYZ,
    244: RTKXYZ,
    249: AUXDEF,
    254: BATSTATUS,
    256: PDCSTATS,
    259: GPGGARTK,
    260: RTCM1819,
    261: OPTIONS,
    263: INSATT,
    264: INSCOV,
    265: INSPOS,
    266: INSSPD,
    267: INSVEL,
    268: RAWIMU,
    270: SATXYZ,
    272: CHANDEBUGFFTPHASE,
    273: CHANDEBUGFFTPOWER,
    274: ISMR,
    275: RTCM9,
    276: RTCM9IN,
    277: POINT,
    278: BASESTATIONOBS,
    279: SATXYZOCC,
    282: RTCM16T,
    283: BASERANGE,
    285: BESTPVC,
    286: POSVELNAVDOP,
    287: RAWWAASFRAME,
    290: WAAS0,
    291: WAAS1,
    292: WAAS10,
    293: WAAS12,
    294: WAAS17,
    295: WAAS18,
    296: WAAS2,
    297: WAAS24,
    298: WAAS25,
    299: WAAS26,
    300: WAAS27,
    301: WAAS3,
    302: WAAS4,
    303: WAAS5,
    304: WAAS6,
    305: WAAS7,
    306: WAAS9,
    307: RTCM15,
    308: RTCM15IN,
    309: ENVIRONMENT,
    310: CMRDESC,
    311: POSVELNAV,
    313: WAASCORR,
    317: COMCONFIG,
    319: INSATTS,
    320: INSCOVS,
    321: INSPOSS,
    322: INSPOSSYNC,
    323: INSSPDS,
    324: INSVELS,
    325: RAWIMUS,
    326: DETRSIN,
    327: RAWSIN,
    330: CLASSELEMLOG,
    332: CLASSLIST,
    334: CLASSREQLOG,
    335: ENUMLIST,
    337: ENUMREQLOG,
    338: MSGIDLIST,
    340: MSGREQLOG,
    341: TYPELIST,
    343: TYPEREQLOG,
    347: RTCAEPHEM,
    348: RTCAEPHEMIN,
    373: HEIGHTMODELSTATUS,
    374: RTCM2021,
    375: NOISEFLOOR,
    378: INSBIASES,
    381: INSLIGHTS,
    384: INSKCOV,
    385: INSKINIT,
    386: INSKSTATE,
    387: INSSYSTEM,
    389: CMRDATADESC,
    390: CMRDATAOBS,
    391: CMRDATAREF,
    392: RTCADATA1,
    393: RTCADATAEPHEM,
    394: RTCADATAOBS,
    395: RTCADATAREF,
    396: RTCMDATA1,
    397: RTCMDATA15,
    398: RTCMDATA16,
    399: RTCMDATA1819,
    400: RTCMDATA2021,
    401: RTCMDATA22,
    402: RTCMDATA3,
    403: RTCMDATA59,
    404: RTCMDATA9,
    407: RAWGPSWORD,
    408: PDC_VERSIONDATA,
    410: PDC_SATDATA,
    420: POINTM,
    423: BESTGPSPOS,
    442: PSRDIFFIN,
    443: PSRDIFFOUT,
    469: PDPPOS,
    470: PDPVEL,
    471: PDPXYZ,
    492: TIMESYNC,
    502: MEMSINSGPS,
    506: BESTGPSVEL,
    507: INSPVA,
    508: INSPVAS,
    513: RAWIMUSUMS,
    520: APPLICATIONSTATUS,
    521: GPGGALONG,
    603: INSSTATENVM,
    606: TYPEENUMS,
    615: MARK2POS,
    616: MARK2TIME,
    622: TIMEDWHEELDATA,
    631: RANGEGPSL1,
    643: CBITHINT,
    644: DEBUGETHERRSRC,
    645: TIMEDMAGDATA,
    646: WHEELSIZE,
    651: SATVISSYS,
    660: RTCMDATA59FKP,
    661: RTCM59FKPIN,
    662: RTCM59FKP,
    663: RTCMDATA23,
    664: RTCMDATA24,
    665: RTCM23,
    666: RTCM23IN,
    667: RTCM24,
    668: RTCM24IN,
    669: RAWIMUIFCARDPACKET,
    671: IMUCARDDEBUG,
    672: IMUCARDSTATUS,
    673: IMUCARDVERSION,
    674: BESTLEVERARM,
    677: SOLVEDLEVERARM,
    686: BSLNXYZ,
    692: DEBUGETHERRSRC2,
    693: DEBUGETHERS2,
    696: WAAS32,
    697: WAAS33,
    698: WAAS34,
    699: WAAS35,
    700: WAAS45,
    703: FKPCORRECTIONS,
    712: CMRPLUSIN,
    716: MMTRAWDATA,
    717: CMRPLUS,
    718: GLOALMANAC,
    719: GLOCLOCK,
    720: GLORAWALM,
    721: GLORAWFRAME,
    722: GLORAWSTRING,
    723: GLOEPHEMERIS,
    726: BESTUTM,
    727: VISIONCALDATA,
    732: RAWLBANDFRAME,
    733: RAWLBANDPACKET,
    747: RAWNAVMSGDATA,
    754: GROUPCOMCONFIG,
    756: INSUTM,
    757: INSUPDATE,
    758: INSRB,
    759: VISIONREFFUNC,
    760: VISIONSOL,
    764: RTCM1005IN,
    765: RTCM1005,
    767: RTCM1006IN,
    768: RTCM1006,
    769: RTCM1004IN,
    770: RTCM1004,
    771: RTCM1001IN,
    772: RTCM1001,
    773: RTCM1002IN,
    774: RTCM1002,
    775: RTCM1003IN,
    776: RTCM1003,
    784: RTCMDATA1001,
    785: RTCMDATA1002,
    786: RTCMDATA1003,
    787: RTCMDATA1004,
    788: RTCMDATA1005,
    789: RTCMDATA1006,
    792: GLORAWEPHEM,
    794: PRXSTATUS,
    797: AUDIOCFGDEF,
    798: EXTLEVELS,
    799: PWRSTATUS,
    805: RTCAOBS2,
    806: RTCAOBS2IN,
    807: RTCA2IN,
    808: RTCADATA2OBS,
    812: CORRIMUDATA,
    813: CORRIMUDATAS,
    816: VISIONREFLIST,
    832: RAWLBANDPREVITERBI,
    833: RTCM1014,
    834: RTCM1014IN,
    843: EXTRXHWLEVELS,
    852: RTCM1007,
    853: RTCM1007IN,
    854: RTCM1008,
    855: RTCM1008IN,
    856: RTCMDATA1007,
    857: RTCMDATA1008,
    859: GLMLA,
    864: RTCM31,
    865: RTCM31IN,
    866: RTCM34,
    867: RTCM34IN,
    868: RTCMDATA31,
    869: RTCMDATA34,
    873: RTCM32,
    874: RTCM32IN,
    875: RTCM36,
    876: RTCM36IN,
    877: RTCM36T,
    878: RTCMDATA32,
    879: RTCMDATA36,
    881: PSRTIME,
    882: CMRGLOOBS,
    883: CMRGLOOBSIN,
    885: RTCM1009,
    886: RTCM1009IN,
    887: RTCM1010,
    888: RTCM1010IN,
    889: RTCM1011,
    890: RTCM1011IN,
    891: RTCM1012,
    892: RTCM1012IN,
    893: RTCM1019,
    894: RTCM1019IN,
    895: RTCM1020,
    896: RTCM1020IN,
    897: RTCMDATA1009,
    898: RTCMDATA1010,
    899: RTCMDATA1011,
    900: RTCMDATA1012,
    901: RTCMDATA1019,
    902: RTCMDATA1020,
    903: RTCM59GLO,
    904: RTCM59GLOIN,
    905: RTCMDATA59GLO,
    918: EXTREFSTATION,
    952: RTKDOP,
    963: HWMONITOR,
    964: RTCMDATA22GG,
    971: HEADING,
    973: RAWSBASFRAME,
    974: RAWGLOFRAME,
    975: RAWGLOSTRING,
    976: SBAS0,
    977: SBAS1,
    978: SBAS10,
    979: SBAS12,
    980: SBAS17,
    981: SBAS18,
    982: SBAS2,
    983: SBAS24,
    984: SBAS25,
    985: SBAS26,
    986: SBAS27,
    987: SBAS3,
    988: SBAS32,
    989: SBAS33,
    990: SBAS34,
    991: SBAS35,
    992: SBAS4,
    993: SBAS45,
    994: SBAS5,
    995: SBAS6,
    996: SBAS7,
    997: SBAS9,
    998: SBASCORR,
    1003: CMRDATAGLOOBS,
    1012: RTCM1037,
    1013: RTCM1037IN,
    1014: RTCM1038,
    1015: RTCM1038IN,
    1016: RTCM1039,
    1017: RTCM1039IN,
    1021: RTCM1015,
    1022: RTCM1015IN,
    1024: RTCM1016,
    1025: RTCM1016IN,
    1027: RTCM1017,
    1028: RTCM1017IN,
    1030: RTCM1036,
    1031: RTCM1036IN,
    1033: RTCM1034,
    1034: RTCM1034IN,
    1036: RTCM1035,
    1037: RTCM1035IN,
    1043: SATVIS2,
    1045: GPHDT,
    1046: HWCONFIGTABLE,
    1047: DEBUGFIQ,
    1048: GLORAWL2FRAME,
    1049: RTCAREFEXT,
    1050: RTCAREFEXTIN,
    1051: MASTERPOS,
    1052: ROVERPOS,
    1053: HEADINGDEBUG,
    1066: RAWCNAVFRAME,
    1067: MARK1PVA,
    1068: MARK2PVA,
    1073: CONFIRMCODE,
    1075: MARK3TIME,
    1076: MARK4TIME,
    1078: MFGTESTRESULTS,
    1079: SIGNALCONFIGURATION,
    1085: PDPSTAT,
    1093: MARK1COUNT,
    1094: MARK2COUNT,
    1095: MARK3COUNT,
    1096: MARK4COUNT,
    1097: RTCM1033,
    1098: RTCM1033IN,
    1099: RTCMDATA1033,
    1108: DLLINFO,
    1110: CHANRESETEVENT,
    1111: PLLINFO,
    1118: MARK3PVA,
    1119: MARK4PVA,
    1120: GALALMANAC,
    1121: GALCLOCK,
    1122: GALEPHEMERIS,
    1123: GALFNAVRAWALMANAC,
    1124: GALFNAVRAWEPHEMERIS,
    1125: GALINAVRAWALMANAC,
    1126: GALINAVRAWEPHEMERIS,
    1127: GALIONO,
    1130: MARK1TIME,
    1131: BASEANTENNAIN,
    1132: HEADINGEXT,
    1133: HEADINGEXTIN,
    1136: GIOVEFNAVRAWFRAME,
    1137: GIOVEINAVRAWFRAME,
    1138: GIOVEFNAVRAWEPHEMERIS,
    1139: GIOVEFNAVRAWALMANAC,
    1140: GIOVEINAVRAWEPHEMERIS,
    1141: GIOVEINAVRAWALMANAC,
    1143: OUTPUTUNDULATION,
    1146: LOGFILESTATUS,
    1148: CHANCONFIGLIST,
    1151: RTCMDATAV3USER,
    1152: RTCMV3USER,
    1153: RTCMV3USERDATA,
    1154: RTCMV3USERIN,
    1156: SBASCORRECTIONS,
    1157: HASSSTATUS,
    1158: LASSSTATUS,
    1159: RANGECORRECTIONS,
    1160: CLOCKSTEERINGADJUSTMENT,
    1161: PACKAGEDOBSERVATIONS,
    1162: PSRSATS,
    1163: PSRDOP2,
    1164: PSRTIME2,
    1169: PROPAGATEDCLOCKMODEL2,
    1170: CLOCKMODEL2,
    1171: PSRCHANNELSTATUS,
    1172: RTKDOP2,
    1173: SBASFAST,
    1174: RTKSATS,
    1176: MATCHEDSATS,
    1177: PASHR,
    1179: PSRINTEGRITYEVENT,
    1180: DEBUGETHER,
    1181: DEBUGETHEREXCEEDED,
    1182: SBASMASK,
    1183: DEBUGCHANMAP,
    1186: ELEVCUTOFFDEBUG,
    1187: SIMULATEDOBSERRORS,
    1189: SIMULATEOBSERRORSTATUS,
    1190: SBASSLOW,
    1191: RAWLBANDCOMDATA,
    1192: GRIDIONO,
    1193: GPGSTDATA,
    1194: BESTSATS,
    1195: PSRRESIDUALS,
    1201: LBANDTRACKSTAT,
    1212: IONOTROPO2,
    1220: TILTDATA,
    1227: GPVTGDATA,
    1228: MAGNETICDECLINATION,
    1229: PSRVEL2,
    1230: GPRMCDATA,
    1231: RTKVEL2,
    1232: BESTVEL2,
    1233: PDPVEL2,
    1234: PDPSATS,
    1235: SOFTLOADSTATUS,
    1236: SOFTLOADDEBUG,
    1238: DEBUGIQDATA,
    1256: BESTLEVERARM2,
    1258: TAGGEDMARK1PVA,
    1259: TAGGEDMARK2PVA,
    1262: GPGRSDATA,
    1266: DEBUGBUFFER,
    1267: RXSTATUSUPDATE,
    1269: DDCDEBUG,
    1270: IMUTOANTOFFSETS,
    1271: BASEIONO,
    1273: RANGECMP2,
    1286: RAIMSTATUS,
    1288: ETHSTATUS,
    1289: IPSTATUS,
    1305: IMURATEPVAS,
    1306: FRONTENDDATA,
    1307: DEBUGBUFFERCMP,
    1308: DEBUGETHERREQUESTORS,
    1309: GALINAVEPHEMERIS,
    1310: GALFNAVEPHEMERIS,
    1314: ALIGNBSLNXYZ,
    1315: ALIGNBSLNENU,
    1316: HEADINGSATS,
    1320: VARIABLELEVERARM,
    1321: GIMBALLEDPVA,
    1325: REFSTATIONINFO,
    1327: TAGGEDMARK3PVA,
    1328: TAGGEDMARK4PVA,
    1329: MODELFEATURES,
    1330: QZSSRAWSUBFRAME,
    1331: QZSSRAWEPHEM,
    1332: ALIGNDOP,
    1335: HEADING2,
    1336: QZSSEPHEMERIS,
    1340: RTCAOBS3,
    1341: RTCAOBS3IN,
    1344: SOURCETABLE,
    1345: QZSSRAWALMANAC,
    1346: QZSSALMANAC,
    1347: QZSSIONUTC,
    1348: AUTHCODES,
    1349: GENERATEALIGNCORRECTIONS,
    1357: SBASHANDLERSSTATUS,
    1358: SBASHANDLEREVENT,
    1362: IMURATECORRIMUS,
    1366: RTCM4093TYPE0,
    1367: RTCM4093IN,
    1368: RTCM4093TYPE1,
    1369: RTCM4093TYPE2,
    1370: RTCM4093TYPE3,
    1371: RTCM4093TYPE4,
    1372: INSUPDATEDEBUG,
    1379: RTKATMOSPHEREDELAYS,
    1380: RTKAMBIGUITIES,
    1381: MOTION,
    1382: HEAVE,
    1389: ISMRAWOBS,
    1390: ISMRAWTEC,
    1393: ISMREDOBS,
    1394: ISMREDTEC,
    1395: ISMDETOBS,
    1402: EXTERNALPOS,
    1403: DECODEDBASESTATIONOBS,
    1406: ISMCALIBRATIONSTATUS,
    1412: PROFILEINFO,
    1413: GALFNAVRAWPAGE,
    1414: GALINAVRAWWORD,
    1421: THISANTENNAIN,
    1422: BASEANTENNAPCCORRECTION,
    1423: THISANTENNAPCCORRECTION,
    1425: SBASALMANAC,
    1426: CORRECTIONSTATS,
    1429: BESTGNSSPOS,
    1430: BESTGNSSVEL,
    1432: RAWIMUCOMDATAS,
    1433: SYNCTIMETRIGGER,
    1446: RELINSPVA,
    1451: SATXYZ2,
    1453: RTKNETWORKGEOMETRICDELAYS,
    1454: RTKNETWORKIONOSPHERICDELAYS,
    1455: MACNETWORK,
    1456: TSS1,
    1457: INSATTX,
    1458: INSVELX,
    1459: INSPOSX,
    1461: RAWIMUX,
    1462: RAWIMUSX,
    1463: EXTERNALPVAS,
    1465: INSPVAX,
    1466: INSLEVERARMS,
    1467: INSOFFSETS,
    1470: INSVARIABLELEVERARMS,
    1472: RTCM1071,
    1473: RTCM1072,
    1474: RTCM1073,
    1475: RTCM1074,
    1476: RTCM1075,
    1477: RTCM1076,
    1478: RTCM1077,
    1479: RTCM1081,
    1480: RTCM1082,
    1481: RTCM1083,
    1482: RTCM1084,
    1483: RTCM1085,
    1484: RTCM1086,
    1485: RTCM1087,
    1486: RTCM1091,
    1487: RTCM1092,
    1488: RTCM1093,
    1489: RTCM1094,
    1490: RTCM1095,
    1491: RTCM1096,
    1492: RTCM1097,
    1494: MATCHEDRESET,
    1496: RTKGLOBIAS,
    1499: LEDSTATES,
    1500: GPSCNAVEPHEM,
    1501: GPSRAWCNAVEPHEM,
    1502: GPSCNAVMIDIALM,
    1503: GPSRAWCNAVMIDIALM,
    1504: GPSCNAVREDUCEDALM,
    1505: GPSRAWCNAVREDUCEDALM,
    1506: GPSCNAVIONO,
    1507: GPSCNAVGROUPDELAY,
    1508: GPSCNAVUTC,
    1509: GPSCNAVEOP,
    1510: GPSCNAVGGTO,
    1511: GPSRAWCNAVMESSAGE,
    1514: CELLINFO,
    1516: CELLSTATUS,
    1518: CAKEPOS,
    1519: CAKEXYZ,
    1520: CAKESATS,
    1521: CAKETIME,
    1522: CAKEVEL2,
    1523: CAKEVEL,
    1526: SINGLEPOINTRESIDUALS,
    1528: SINGLEPOINTOUTLIERS,
    1529: CAKELOG,
    1530: QZSSRAWCNAVMESSAGE,
    1531: MODULEPOWER,
    1533: GPSNAVCDC,
    1534: GPSNAVEDC,
    1537: FAULT,
    1538: PPPPOS,
    1541: PPPSATS,
    1543: PPPXYZ,
    1546: PPPDOP2,
    1548: ORBITANDCLOCKCORRECTIONS,
    1554: PPPFILTERPOS,
    1556: PPPEARTHTIDES,
    1557: PPPFASTRESIDUALS,
    1558: PPPRESIDUALS,
    1562: PPPSYSTEMBIASES,
    1563: PPPINTEGRITYEVENT,
    1564: PPPOUTLIERS,
    1565: GROUPDELAYS,
    1567: PPPLOG,
    1569: BDSB1RAWNAVSUBFRAME,
    1570: RTCAREFPVA,
    1571: RTCAREFPVAIN,
    1572: RELINSPVAIN,
    1580: USERACCOUNTS,
    1583: BDSB1EPHEMERIS,
    1584: BDSALMANAC,
    1585: BDSALMANACHEALTH,
    1590: BDSIONO,
    1591: RTCM4093TYPE5,
    1592: RTCM1121,
    1593: RTCM1122,
    1594: RTCM1123,
    1595: RTCM1124,
    1596: RTCM1125,
    1597: RTCM1126,
    1598: RTCM1127,
    1599: NOVATELXGPSOBS,
    1600: NOVATELXGLOOBS,
    1601: NOVATELXSBASOBS,
    1602: NOVATELXGALOBS,
    1603: NOVATELXQZSSOBS,
    1604: NOVATELXBDSOBS,
    1607: BDSCLOCK,
    1608: BLUETOOTHSTATUS,
    1613: WIFICLISTATUS,
    1616: WIFICLISCANRESULTS,
    1618: NOVATELXOBS,
    1619: NOVATELXOBSIN,
    1620: NOVATELXREF,
    1621: NOVATELXREFIN,
    1622: PPPTROPODELAYS,
    1624: DEBUGDATA,
    1630: NOVATELXREFTEMP,
    1633: RTCM1104BDS,
    1641: RTCM1101,
    1642: RTCM1102,
    1643: RTCM1103,
    1644: RTCM1104,
    1645: RTCM1105,
    1646: RTCM1106,
    1647: RTCM1107,
    1648: RTCM1111,
    1649: RTCM1112,
    1650: RTCM1113,
    1651: RTCM1114,
    1652: RTCM1115,
    1653: RTCM1116,
    1654: RTCM1117,
    1655: RTCM1230,
    1656: RTCM1230IN,
    1657: HEADING3,
    1659: DEBUGVAS,
    1661: HEADINGEXT2,
    1662: HEADINGEXT2IN,
    1666: WIFIAPSTATUS,
    1667: BESTPOSIN,
    1668: HWCONFIGTABLERAW,
    1669: IPSTATS,
    1675: BLUETOOTHDATA,
    1676: PPPTROPOMODEL,
    1685: CELLULARSTATUS,
    1686: CELLULARINFO,
    1695: BDSRAWNAVSUBFRAME,
    1696: BDSEPHEMERIS,
    1697: DEBUGROUTETABLE,
    1698: HEADINGRATE,
    1708: SYNCHEAVE,
    1709: DELAYEDHEAVE,
    1712: VERIPOSDEBUGDATA,
    1714: PPPSEEDSTORE,
    1715: RTCMV2DATAIN,
    1716: RTCMV3DATAIN,
    1717: NOVATELXRTCMV3SSRIN,
    1718: LBANDBEAMTABLE,
    1719: TERRASTARINFO,
    1721: PPPFILTERSATS,
    1724: VERIPOSMESSAGE,
    1725: VERIPOSRTCMDATA,
    1726: VERIPOSMESSAGETYPES,
    1727: VERIPOSSTANDARDSTATIONS,
    1728: VERIPOSINFO,
    1729: TERRASTARSTATUS,
    1730: VERIPOSSTATUS,
    1731: VERIPOSEXTENDEDINFO,
    1732: DEBUGTXBUFFERS,
    1734: RANGECMP3,
    1737: VERIPOSNVMDATA,
    1738: MARK3POS,
    1739: MARK4POS,
    1743: SYNCRELINSPVA,
    1744: DEBUGPROCESSRUNTIMES,
    1748: EM3000,
    1752: TRACKSUMMARY,
    1754: PPPSEEDSIGNALS,
    1755: PPPDETECTEDDYNAMICS,
    1756: PPPFASTLOG,
    1757: PPPFASTGROSSOUTLIERS,
    1758: PPPVEL,
    1759: PPPVEL2,
    1762: DEBUGPROCESSMEMUSAGE,
    1764: GENERATEINSALIGNCORRECTIONS,
    1768: GPHCD,
    1769: BDXT1,
    1770: PTNL,
    1771: GPTRA,
    1772: GPNTR,
    1777: UPTIME,
    1778: IMURATEPVA,
    1780: RTKFASTLOG,
    1781: BESTSEEDPOS,
    1782: STEADYLINESTATE,
    1783: STEADYLINEINTERNALSTATE,
    1787: DEBUGCONTEXTSWITCH,
    1798: ALIGNSTATS,
    1802: PAVSTATUS,
    1803: RTKSEEDSIGNALS,
    1804: RTKFASTRESIDUALS,
    1805: RTKFASTIONO,
    1807: RTKBASEIONO,
    1808: RTKBASESATELLITECLOCKS,
    1809: RTKBASELOG,
    1811: PDPFASTLOG,
    1812: PDPFASTIONO,
    1813: PDPFILTERPOS,
    1814: PDPFASTRESIDUALS,
    1815: PDPFILTERSATS,
    1818: CELLULARACTIVATESTATUS,
    1819: CELLULARIPSTATUS,
    1823: PDPFILTERSTAT,
    1824: PDPFILTERVEL,
    1825: INSUPDATESTATUS,
    1847: PDPDETECTEDDYNAMICS,
    1849: DECODEDBASESTATIONREF,
    1850: PDPDELTAPHASEVEL,
    1854: PPPFASTFEEDBACK,
    1858: DECODEDDIFFERENTIALCORRECTIONS,
    1859: DECODEDBASESTATION,
    1862: VERIPOSPERSISTENTSTATIONS,
    1863: PSRDIFFSTATIONS,
    1864: VERIPOSRTCMPORTDATA,
    1867: ORBITANDCLOCKCORRECTIONSINFO,
    1869: GPGNS,
    1873: SAMPLEBUFFERDATA,
    1875: HIGHRESBINDATA,
    1876: CORRECTIONSQUALITY,
    1877: RADARSTATUS,
    1880: CANDATA,
    1881: COARSETIMEOFFSET,
    1883: PPPFASTIONO,
    1884: PGN129025,
    1885: PGN129026,
    1886: PGN129027,
    1887: PGN129029,
    1888: PGN126992,
    1889: INSPVACMP,
    1890: INSPVASDCMP,
    1896: DEBUGPOOLSTATISTICS,
    1897: DEBUGEXHAUSTEDBROKERS,
    1899: DEBUGPACKETPOOL,
    1900: DEBUGBROKERINFO,
    1901: DEBUGPACKETUSAGE,
    1904: PPPFASTSEEDPOS,
    1905: INITIALINSSTATEINFO,
    1907: J1939STATUS,
    1910: PDPLOG,
    1911: SATELLITEPCV,
    1912: DEBUGMEMUSAGE,
    1913: DEBUGIDLESTATS,
    1916: DEBUGEVENTSCONFIG,
    1922: DEBUGPROVIDERINFO,
    1928: PGN129551,
    1931: SORTEDSIGCHANMAP,
    1933: LBANDDECODEDFRAME,
    1934: LBANDENCODEDFRAME,
    1935: LBANDSOFTSYMFRAME,
    1945: INSCONFIG,
    1951: SAVEDSURVEYPOSITIONS,
    1953: DEBUGLARGESTMESSAGES,
    1961: INSCALSTATUS,
    1966: DEBUGBOOTTIMES,
    1968: ITPSDFINAL,
    1969: VERIPOSMESSAGESTATS,
    1971: DEBUGLOGGINGSUMMARY,
    1976: DEBUGLOGGINGPACKETFLOW,
    1978: PFHIGHRESBINDATA,
    1979: CLOCKSTEERINGINPUT,
    1980: INSOFFSETS2,
    1981: DEBUGLOGGINGSEQUENTIAL,
    1982: PDPVELLOG,
    1986: ITPSDRAW,
    1987: INSUPDATESOLUTION,
    1988: MULTIPATHCONDITIONS,
    1990: ITFILTCOEFTABLE,
    1991: ITFILTTABLE,
    1995: PDPDOP2,
    1996: BESTFASTLOG,
    1997: PPPDOP,
    1998: PDPDOP,
    2005: DEBUGENCRYPTIONKEY,
    2006: DEBUGDECRYPTIONKEY,
    2007: DEBUGLOGGINGPUBLISHLATENCY,
    2008: TRACKINGDOP,
    2009: TRACKINGDOP2,
    2010: VERIPOSTRACKSTAT,
    2011: INHDT,
    2015: ENCRYPTIONSTATUS,
    2016: DECRYPTIONSTATUS,
    2018: SRTKSUBSCRIPTIONS,
    2021: DEBUGIRQ,
    2022: ITBANDPASSBANK,
    2023: ITPROGFILTBANK,
    2024: DEBUGPROVIDERREQUESTS,
    2026: WEBSERVERINFO,
    2027: CLIENTSESSIONINFO,
    2028: EDRDATA,
    2030: VERIPOSBESTSOLUTION,
    2031: VERIPOSSOLUTIONS,
    2032: VERIPOSUKOOASENTENCE,
    2034: TMRI,
    2035: PSRINTEGRITYDETAIL,
    2040: PPPINTEGRITYDETAIL,
    2041: PPPFASTINTEGRITYDETAIL,
    2042: DUALANTENNAHEADING,
    2043: DUALANTENNAHEADINGDATAREQUEST,
    2045: GPHDTDUALANTENNA,
    2046: ITREFLEVEL,
    2047: WEBUICLIENTINFO,
    2048: RTKASSISTSTATUS,
    2049: PPPINTERNALPOS,
    2050: RANGECMP4,
    2051: INSSTDEV,
    2052: INSSTDEVS,
    2053: RTKASSISTSTATUSDEBUG,
    2054: RTKMATCHEDFEEDBACK,
    2057: PPPCORRECTIONDRIFT,
    2060: SAFEMODESTATUS,
    2063: ITPSDDETECT,
    2065: ITDETECTSTATUS,
    2069: LBANDRAWFRAME,
    2074: TERRASTARBEAMSTATUS,
    2075: VERIPOSDECODERSTATUS,
    2076: VERIPOSPORTDATA,
    2077: ALIGNCORRDIAG,
    2078: RTKCORRDIAG,
    2079: TRACKDIAG,
    2080: PDPDIAG,
    2081: VERIPOSDECODEREVENT,
    2083: FRONTENDGAIN,
    2084: VERIPOSRTCMDATAEXT,
    2086: VERIPOSSTATIONS,
    2088: RTCM1019ASYNC,
    2089: RTCM1020ASYNC,
    2092: IPDEBUGSTATS,
    2093: WIFIAPSETTINGS,
    2094: WIFIAPDEBUG,
    2097: PPPFILTERINTEGRITYDETAIL,
    2098: ITPSDCALIBRATIONDATA,
    2100: FILELIST,
    2101: FILETRANSFERSTATUS,
    2104: FILESYSTEMSTATUS,
    2105: NAVICRAWSUBFRAME,
    2106: ITFRONTENDDATA,
    2108: WIFIACCESSPOINTSTATUS,
    2111: SIGDETDEBUGBUFFER,
    2112: SIGDETDEBUGACQ,
    2114: TRANSFERPORTSTATUS,
    2118: INSATTQS,
    2122: NAVICALMANAC,
    2123: NAVICEPHEMERIS,
    2124: NAVICIONO,
    2125: NAVICSYSCLOCK,
    2127: FILESTATUS,
    2129: INSSEEDSTATUS,
    2131: DUALANTENNAHEADING2,
    2132: MATCHEDXYZCOV,
    2136: DEBUGMINPERFORMANCEDATA,
    2137: FILESYSTEMCAPACITY,
    2141: ITDETECTDEBUG,
    2142: ITRAWSAMPLES,
    2146: DEBUGRANGEINFO,
    2148: SIMULATEDSATELLITESMAPPING,
    2150: LUAFILESYSTEMSTATUS,
    2151: LUAFILELIST,
    2152: LUASTATUS,
    2156: SDDRDATA,
    2157: PPPAMBIGUITIES,
    2158: KSXT,
    2159: OCEANIXINFO,
    2160: OCEANIXSTATUS,
    2161: VERIPOSSTATUSDEBUG,
    2162: INSMOTIONDETECT,
    2170: RTCM1042ASYNC,
    2171: RTCM1042,
    2172: RTCM1045ASYNC,
    2173: RTCM1045,
    2174: RTCM1046ASYNC,
    2175: RTCM1046,
    2176: RTCM1044ASYNC,
    2177: RTCM1044,
    2178: PPPSTATESPACEDATA,
    2183: ITDETECTIONMASK,
    2185: RAWSBASFRAME2,
    2186: SATELLITEGDV,
    2187: PPPIONORESIDUALS,
    2188: PPPIONO,
    2196: RTKMATCHEDLOG,
    2198: ITFRONTENDCONFIGURATION,
    2201: DEBUGTRANSACTIONLOG,
    2202: BASEPOS,
    2205: SATELSTATUS,
    2207: WIFISTATUS,
    2208: DEBUGUSBSTATS,
    2209: QZSSL6PRNRAMCODE,
    2210: WIFINETLIST,
    2216: SATEL4INFO,
    2220: SATEL9INFO,
    2227: COARSETIMEOFFSET2,
    2228: ALIGNCORRREQUEST,
    2229: SSRDATAINFO,
    2234: USERI2CRESPONSE,
    2239: GALCNAVRAWPAGE,
    2240: LUAOUTPUT,
    2242: SIMULATESATELLITEERRORSTATUS,
    2243: SIMULATEDSATELLITEERRORS,
    2244: DEBUGRETRIEDBROKERS,
    2245: INPUTPARSERSTATUS,
    2247: ANNOTATIONCMP,
    2250: PPPSEEDAPPLICATIONSTATUS,
    2251: PPPSEEDSTORESTATUS,
    2252: DEBUGSIGCHANASSIGN,
    2253: SIGNALACQSTATS,
    2257: TIMETOPOSITIONEVENT,
    2261: QZSSCNAVRAWMESSAGE,
    2262: GPSCNAVRAWMESSAGE,
    2263: RANKLIST,
    2264: CORRIMUS,
    2266: PPPMANAGERSTATUS,
    2267: SSRCORRECTIONSDIGEST,
    2272: MARKDMIPVAS,
    2273: PPPINTERNALSEED,
    2274: SPRINKLERDATA,
    2276: SPRINKLERDATAH,
    2277: VERIPOSREGIONALBEAM,
    2278: VERIPOSPERMISSIONS,
    2279: VERIPOSRTCMV3DATA,
    2282: USERANTENNA,
    2285: MCMFSTATUS,
    2286: LBANDRAWFRAME2,
    2287: VERIPOSTRINAVSENTENCE,
    2291: TECTONICSCOMPENSATION,
    2292: SSRDATUMINFO,
    2293: PPPDATUMINFO,
    2294: PPPFASTMETADATA,
    2296: GEODETICDATUMS,
    2298: DATUMTRANSFORMATIONS,
    2299: EXPANDEDDATUM,
    2300: PSRDATUMINFO,
    2301: CAKEDATUMINFO,
    2302: BESTGNSSDATUMINFO,
    2303: PDPDATUMINFO,
    2304: RTKDATUMINFO,
    2305: BESTDATUMINFO,
    2307: TILTBIASES,
    2308: PMDT,
    2310: TILTSTATUS,
    2317: BLUETOOTHNAME,
    2318: INSVELUSER,
    }
