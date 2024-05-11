from PyQt5 import QtWidgets, QtCore


from generated_ui import Ui_MainWindow
from generated_dialog import Ui_CustomSquare

from net import LTENetwork

class UiDialog(QtWidgets.QWidget):
    def __init__(self):
        super(UiDialog, self).__init__()

        self.ui = Ui_CustomSquare()
        self.ui.setupUi(self)

class calcNetUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(calcNetUi, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dialog = UiDialog()

        self.custom_square = 0

        self.setupFunctionality()

    def setupFunctionality(self):
        self.ui.CalcNetButton.clicked.connect(self.calculateNet)

        self.ui.CustomSquareButton.clicked.connect(self.openDialog)
        self.dialog.ui.ConfirmCustomZonebutton.clicked.connect(self.setCustomSquare)

    def openDialog(self):
        
        self.dialog.show()

    def setCustomSquare(self):
        try:
            self.custom_square = int(self.dialog.ui.lineEdit_CustomSquare.text())
        except ValueError:
            self.dialog.ui.lineEdit_CustomSquare.setStyleSheet("background-color: rgba(245, 39, 39, 0.43); border-radius:5px; border: 1px solid #dcdcdc;")
        else:
            self.dialog.ui.lineEdit_CustomSquare.setStyleSheet("background-color: #ffffff; border-radius:5px; border: 1px solid #dcdcdc;")
            self.dialog.ui.lineEdit_CustomSquare.clear()
            self.dialog.close()

    def calculateNet(self):
        isOkCounter = 0

        try:
            list_num = int(self.ui.lineEdit_ListNumber.text())
            isOkCounter+=1
        except ValueError:
            self.ui.lineEdit_ListNumber.setStyleSheet("background-color: rgba(245, 39, 39, 0.43); border-radius:5px; border: 1px solid #dcdcdc;")
            isOkCounter-=1
        else:
            self.ui.lineEdit_ListNumber.setStyleSheet("background-color: rgba(51, 245, 39, 0.43);; border-radius:5px; border: 1px solid #dcdcdc;")

        try:
            zach_num = self.ui.lineEdit_ZachNumber.text()
            test = int(zach_num.strip())

            isOkCounter+=1
        except ValueError:
            self.ui.lineEdit_ZachNumber.setStyleSheet("background-color: rgba(245, 39, 39, 0.43); border-radius:5px; border: 1px solid #dcdcdc;")
            isOkCounter-=1
        else:
            self.ui.lineEdit_ZachNumber.setStyleSheet("background-color: rgba(51, 245, 39, 0.43);; border-radius:5px; border: 1px solid #dcdcdc;")

        try:
            cluster_sz = int(self.ui.lineEdit_ClusterSize.text())
            isOkCounter+=1
        except ValueError:
            self.ui.lineEdit_ClusterSize.setStyleSheet("background-color: rgba(245, 39, 39, 0.43); border-radius:5px; border: 1px solid #dcdcdc;")
            isOkCounter-=1
        else:
            self.ui.lineEdit_ClusterSize.setStyleSheet("background-color: rgba(51, 245, 39, 0.43);; border-radius:5px; border: 1px solid #dcdcdc;")

        if isOkCounter == 3:
            for i in [self.ui.lineEdit_ListNumber, self.ui.lineEdit_ZachNumber, self.ui.lineEdit_ClusterSize]:
                i.setStyleSheet("background-color: rgba(51, 245, 39, 0.43); border-radius:5px; border: 1px solid #dcdcdc;")

            
            if self.custom_square != 0:
                lte = LTENetwork(list_num, zach_num, cluster_sz, self.custom_square)
            else:
                lte = LTENetwork(list_num, zach_num, cluster_sz)

            self.displayValues(lte)

    def displayValues(self, lte_net : LTENetwork):
        # Параметры зоны
        self.ui.label_Square_Var.setText(f"{lte_net.s:.3f}")
        self.ui.label_SubsQuant_Var.setText(f"{lte_net.subscribers_quant:.3f}")
        self.ui.label_SubsActivity_Var.setText(f"{lte_net.subscriber_activity:.3f}")
        self.ui.label_BlockProb_Var.setText(f"{lte_net.call_block_prob:.3f}")
        self.ui.label_ChannelsPerSector_Var.setText(f"{lte_net.channels_per_sector:.3f}")
        self.ui.label_TalkChannels_Var.setText(f"{lte_net.na:.3f}")
        self.ui.label_BandPerChannel_Var.setText(f"{lte_net.fk:.3f}")

        # Параметры кластера
        self.ui.label_SignalLevelDev_Var.setText(f"{lte_net.sigma:.3f}")
        self.ui.label_SignalNoise_Var.setText(f"{lte_net.signal_noise:.3f}")
        self.ui.label_AcceptableProb_Var.setText(f"{lte_net.available_prob:.3f}")
        self.ui.label_ClusterSize_Var.setText(f"{lte_net.cluster_size:.3f}")
        self.ui.label_SectorsQuant_Var.setText(f"{lte_net.sectors_quant:.3f}")
        self.ui.label_TrafficChannelsQuant_Var.setText(f"{lte_net.nn:.3f}")
        self.ui.label_RadioChannelsPerSector_Var.setText(f"{lte_net.nc:.3f}")

        # Up-Down параметры
        self.ui.label_Bandwidth_Var.setText(f"{lte_net.freq:.3f}")
        self.ui.label_BSASPower_Var.setText(f"{lte_net.bs_as_line_power:.3f}")
        self.ui.label_ASBSPower_Var.setText(f"{lte_net.as_bs_line_power:.3f}")
        self.ui.label_BSASFeederLoss_Var.setText(f"{lte_net.bs_as_line_feeder_loss:.3f}")
        self.ui.label_BSASDuplexFilterLoss_Var.setText(f"{lte_net.bs_as_line_feeder_loss:.3f}")
        self.ui.label_BSASDiplexorLoss_Var.setText(f"{lte_net.bs_as_line_duplexor_loss:.3f}")
        self.ui.label_BSASAntennaGain_Var.setText(f"{lte_net.bs_as_line_antenna_gain:.3f}")
        self.ui.label_RecieverSens_Var.setText(f"{lte_net.lines_sensitivity:.3f}")
        self.ui.label_InsideBuildingLoss_Var.setText(f"{lte_net.building_loss:.3f}")
        self.ui.label_InsideSubBodyLoss_Var.setText(f"{lte_net.subscriber_body_loss:.3f}")
        self.ui.label_Correction_Var.setText(f"{lte_net.needed_correction:.3f}")

        # Параметры СПС
        self.ui.label_PK_Var.setText(f"{lte_net.pK:.3f}")
        self.ui.label_FreqChannelsQuant_Var.setText(f"{lte_net.nk:.3f}")
        self.ui.label_MinBandwidth_Var.setText(f"{lte_net.delta_f:.3f}")
        self.ui.label_TalkChannelsQuant_Var.setText(f"{lte_net.ns:.3f}")
        self.ui.label_PhoneLoad_Var.setText(f"{lte_net.a:.3f}")
        self.ui.label_SubsPerSlot_Var.setText(f"{lte_net.nab:.3f}")
        self.ui.label_BSQuant_Var.setText(f"{lte_net.bs_quant:.3f}")
        self.ui.label_SingleBSRadius_Var.setText(f"{lte_net.rc:.3f}")

        # Потери
        self.ui.label_PowerStock_Var.setText(f"{lte_net.z:.3f}")
        self.ui.label_PBSizl_Var.setText(f"{lte_net.p_bs_izl:.3f}")
        self.ui.label_PASizl_Var.setText(f"{lte_net.p_as_izl:.3f}")
        self.ui.label_RecieverSensitivity_Var.setText(f"{lte_net.pch:.3f}")
        self.ui.label_NeededPower_Var.setText(f"{lte_net.pmin:.3f}")
        self.ui.label_BSASSumLoss_Var.setText(f"{lte_net.bs_sum_loss:.3f}")
        self.ui.label_ASBSSumLoss_Var.setText(f"{lte_net.as_sum_loss:.3f}")

        # Затухание сигнала
        self.ui.label_LSelsk_Var.setText(f"{lte_net.l_selsk:.3f}")
        self.ui.label_LprigSmallMedium_Var.setText(f"{lte_net.l_prig_small_medium:.3f}")
        self.ui.label_LprigBig_Var.setText(f"{lte_net.l_prig_big:.3f}")
        self.ui.label_LcitySmallMedium_Var.setText(f"{lte_net.l_city_small_medium:.3f}")
        self.ui.label_LcityBig_Var.setText(f"{lte_net.l_city_big:.3f}")