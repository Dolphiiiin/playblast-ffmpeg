# playblast-ffmpeg
# # description: Playblast and encode with ffmpeg for Maya
# # version: 1.0
#
# Tested on Maya 2025
# Requires ffmpeg.exe in the userScript directory
# UI file: playblast-ffmpeg.ui
#

import os
import subprocess
from maya import cmds

try:
    from PySide2 import QtWidgets, QtGui
    from PySide2.QtUiTools import QUiLoader
except ImportError:
    from PySide6 import QtWidgets, QtGui
    from PySide6.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


UI_FILE_PATH = cmds.internalVar(userScriptDir=True) + '/playblast-ffmpeg.ui'

# UI_FILE_PATHの確認
if not os.path.exists(UI_FILE_PATH):
    raise RuntimeError(f"UI file not found: {UI_FILE_PATH}")

class showUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        # 現在開いているウィンドウから、このUIが開いているか確認して、開かれている場合は閉じる
        for widget in QtWidgets.QApplication.instance().topLevelWidgets():
            if widget.objectName() == 'Playblast ffmpeg':
                widget.close()

        super(showUI, self).__init__(*args, **kwargs)

        # 作ったUIファイルをロードして変数に入れる
        self.widget = QUiLoader().load(UI_FILE_PATH)
        self.setWindowTitle(self.widget.windowTitle())
        self.setCentralWidget(self.widget)
        self.setWindowTitle('Playblast ffmpeg')
        self.resize(self.widget.width(), self.widget.height())
        self.show()

        # ウィンドウが開かれるときにoptionVarから値を取得してウィンドウに反映する
        self.widget_list = [
            ['decoration_checkBox', 'QCheckBox', 0],
            ['polygon_checkBox', 'QCheckBox', 0],
            ['percent_spin', 'QSpinBox', 100],
            ['size_comboBox', 'QComboBox', 1],
            ['customeSize_W', 'QSpinBox', 1280],
            ['customeSize_H', 'QSpinBox', 720],
            ['scale_spin', 'QDoubleSpinBox', 1.0],
            ['padding_spin', 'QSpinBox', 4],
            ['overWrite_checkBox', 'QCheckBox', 1],
            ['openFile_checkBox', 'QCheckBox', 1],
            ['openFolder_checkBox', 'QCheckBox', 0],
            ['fileName_lineEdit', 'QLineEdit', ''],
            ['savePath_lineEdit', 'QLineEdit', ''],
            ['exportPath_lineEdit', 'QLineEdit', 'C:/temp/playblast_temp.avi'],
            ['autoDelete_checkBox', 'QCheckBox', 1],
            ['ffmpegOption_textEdit', 'QTextEdit', '-y -vcodec libx264 -pix_fmt yuv420p -crf 23 -acodec aac -strict -2 '
                                                   '-b:a 384k -movflags faststart '],
            ['ffmpegPath_Default_radioButton', 'QRadioButton', 1],
            ['ffmpegPath_Custome_radioButton', 'QRadioButton', 0],
            ['ffmpegPath_lineEdit', 'QLineEdit', '']
        ]

        # ウィンドウが閉じられるときに、optionVarに値を保存する
        self.reflect_optionVar_to_window(self.widget_list)

        # resetボタンが押されたときに、デフォルト値に戻す
        self.widget.reset_action.triggered.connect(self.reset_widgets)


        # ウィンドウが開かれたときに、size_comboBoxの値をチェック
        self.update_custom_size_enabled()
        # size_comboBoxの値が変更されたときにスロットをトリガー
        self.widget.size_comboBox.currentIndexChanged.connect(self.update_custom_size_enabled)

        # locate_buttonが押されたときに、savePath_lineEditにパスを入れる
        self.widget.locate_button.clicked.connect(self.savePath_locate)

        # export_pushButtonが押されたときに、export_playblast関数を実行
        self.widget.export_pushButton.clicked.connect(self.export_playblast)


    ##### ウィジェットの有効無効を切り替える #####

    def update_custom_size_enabled(self):
        debug("Entering update_custom_size_enabled", 'trace')
        if self.widget.size_comboBox.currentIndex() != 2:
            self.widget.customeSize_W.setEnabled(False)
            self.widget.customeSize_H.setEnabled(False)
        else:
            self.widget.customeSize_W.setEnabled(True)
            self.widget.customeSize_H.setEnabled(True)
        debug("Exiting update_custom_size_enabled", 'trace')

    # ウィンドウが閉じられるときに、optionVarに値を保存する
    def closeEvent(self, event):
        debug("Entering closeEvent", 'trace')
        self.save_widget_values_to_optionVar(self.widget_list)
        debug("Exiting closeEvent", 'trace')
        event.accept()

    # ウィジェットの値をデフォルト値に戻す
    def reset_widgets(self):
        debug("Entering reset_widgets", 'trace')
        for widget_name, widget_type, default_value in self.widget_list:
            widget = getattr(self.widget, widget_name)
            if widget_type == 'QCheckBox' or widget_type == 'QRadioButton':
                widget.setChecked(default_value)
            elif widget_type in ['QSpinBox', 'QDoubleSpinBox']:
                widget.setValue(default_value)
            elif widget_type == 'QComboBox':
                widget.setCurrentIndex(default_value)
            elif widget_type == 'QLineEdit':
                widget.setText(default_value)
            elif widget_type == 'QTextEdit':
                widget.setPlainText(default_value)
            else:
                debug(f"Unsupported widget type: {widget_type} ({widget_name})", 'error')
        debug("Exiting reset_widgets", 'trace')

    def save_widget_values_to_optionVar(self, widget_list):
        debug("Entering save_widget_values_to_optionVar", 'trace')
        for widget_name, widget_type, _ in widget_list:
            widget = getattr(self.widget, widget_name)
            if widget_type == 'QCheckBox' or widget_type == 'QRadioButton':
                cmds.optionVar(intValue=('pbff_'+widget_name, widget.isChecked()))
            elif widget_type in ['QSpinBox', 'QDoubleSpinBox']:
                cmds.optionVar(intValue=('pbff_'+widget_name, widget.value()))
            elif widget_type == 'QComboBox':
                cmds.optionVar(intValue=('pbff_'+widget_name, widget.currentIndex()))
            elif widget_type == 'QLineEdit':
                cmds.optionVar(stringValue=('pbff_'+widget_name, widget.text()))
            elif widget_type == 'QTextEdit':
                cmds.optionVar(stringValue=('pbff_'+widget_name, widget.toPlainText()))
            else:
                debug(f"Unsupported widget type: {widget_type} ({widget_name})", 'error')
        debug("Exiting save_widget_values_to_optionVar", 'trace')

    def reflect_optionVar_to_window(self, widget_list):
        debug("Entering reflect_optionVar_to_window", 'trace')
        for widget_name, widget_type, _ in widget_list:
            if cmds.optionVar(exists='pbff_'+widget_name):
                value = cmds.optionVar(query='pbff_'+widget_name)
                widget = getattr(self.widget, widget_name)
                if widget_type == 'QCheckBox':
                    widget.setChecked(value)
                elif widget_type == 'QSpinBox':
                    widget.setValue(value)
                elif widget_type == 'QDoubleSpinBox':
                    widget.setValue(value)
                elif widget_type == 'QLineEdit':
                    widget.setText(value)
                elif widget_type == 'QComboBox':
                    widget.setCurrentIndex(value)
                elif widget_type == 'QRadioButton':
                    widget.setChecked(value)
                else:
                    debug(f"Unsupported widget type: {widget_type} ({widget_name})", 'error')
        debug("Exiting reflect_optionVar_to_window", 'trace')

    def savePath_locate(self):
        debug("Entering savePath_locate", 'trace')
        # ファイルダイアログを開いて、フォルダを選択する
        savePath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if savePath:
            self.widget.savePath_lineEdit.setText(savePath)
        debug("Exiting savePath_locate", 'trace')


    def export_playblast(self):
        debug("Entering export_playblast", 'trace')
        # バリテーション
        # # fileName_lineEditが空の場合はエラーを出す
        if not self.widget.fileName_lineEdit.text():
            QtWidgets.QMessageBox.critical(self, "Error", "ファイル名を入力してください。")
            cmds.error("Please input file name.")
            return
        # # savePath_lineEditが空の場合はエラーを出す
        if not self.widget.savePath_lineEdit.text():
            QtWidgets.QMessageBox.critical(self, "Error", "保存先を入力してください。")
            cmds.error("Please input save path.")
            return
        
        # # 保存先のフォルダが存在しない場合は、ダイアログで作成するかを確認
        if not os.path.isdir(self.widget.savePath_lineEdit.text()):
            reply = QtWidgets.QMessageBox.question(self, 'フォルダ作成確認', f'{self.widget.savePath_lineEdit.text()} は存在しません。作成しますか？',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                debug("User chose not to create the folder.", 'info')
                return
            os.makedirs(self.widget.savePath_lineEdit.text())

        # # exportPath_lineEditのフォルダ存在しない場合は、ダイアログで作成するかを確認
        if not os.path.isdir(os.path.dirname(self.widget.exportPath_lineEdit.text())):
            reply = QtWidgets.QMessageBox.question(self, 'フォルダ作成確認', f'{os.path.dirname(self.widget.exportPath_lineEdit.text())} は存在しません。作成しますか？',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                debug("User chose not to create the folder.", 'info')
                return
            os.makedirs(os.path.dirname(self.widget.exportPath_lineEdit.text()))
        
        # # ffmpegPath_Custome_radioButtonが1で、ffmpegPath_lineEditが空の場合はエラーを出す
        if self.widget.ffmpegPath_Custome_radioButton.isChecked() and not self.widget.ffmpegPath_lineEdit.text():
            QtWidgets.QMessageBox.critical(self, "Error", "Please input ffmpeg path.")
            cmds.error("Please input ffmpeg path.")
            return

        view = False
        decoration = self.widget.decoration_checkBox.isChecked()
        percent = self.widget.percent_spin.value()
        start_time = cmds.playbackOptions(query=True, min=True)
        end_time = cmds.playbackOptions(query=True, max=True)
        scale = self.widget.scale_spin.value() *100
        frame_padding = self.widget.padding_spin.value()

        # {savePath_lineEdit}/{fileName_lineEdit}.mp4 が存在する場合、上書きするか確認
        savePath = self.widget.savePath_lineEdit.text()
        fileNmae = self.widget.fileName_lineEdit.text() + '.mp4'
        if os.path.exists(f'{savePath}/{fileNmae}'):
            if not self.widget.overWrite_checkBox.isChecked():
                reply = QtWidgets.QMessageBox.question(self, '上書き確認', f'{savePath}/{fileNmae} は既に存在します。上書きしますか？',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    debug("User chose not to overwrite the file.", 'info')
                    return

        

        # widthHeightの値を取得
        if self.widget.size_comboBox.currentIndex() == 1:
            # レンダー設定の解像度を取得
            render_width = cmds.getAttr("defaultResolution.width")
            render_height = cmds.getAttr("defaultResolution.height")
            width_height = (render_width, render_height)
        elif self.widget.size_comboBox.currentIndex() == 2:
            width_height = (self.widget.customeSize_W.value(), self.widget.customeSize_H.value())
        else:
            debug("Unsupported size_comboBox index.", 'error')
            return

        playblast_output_path = self.widget.exportPath_lineEdit.text()

        playblast_options = {
            'format': 'avi',
            'sequenceTime': False,
            'viewer': view,
            'showOrnaments': decoration,
            'percent': percent,
            'startTime': start_time,
            'endTime': end_time,
            'framePadding': frame_padding,
            'clearCache': True,
            'forceOverwrite': True,
            'filename': playblast_output_path,
            'widthHeight': width_height,
        }

        # ポリゴンのみをビューポートで表示する
        if self.widget.polygon_checkBox.isChecked():
            cmds.modelEditor(cmds.playblast(ae=True), edit=True, allObjects=False, polymeshes=True)

        # playblast_output_pathのファイルが存在する場合、削除する
        if os.path.exists(playblast_output_path):
            try:
                os.remove(playblast_output_path)
            except PermissionError:
                # ファイルが使用中の場合、少し待機して再試行
                time.sleep(1)
                try:
                    os.remove(playblast_output_path)
                except PermissionError:
                    QtWidgets.QMessageBox.critical(self, "Error", f"ファイル {playblast_output_path} を削除できません。他のアプリケーションで開かれている可能性があります。")
                    cmds.error(f"Cannot delete file: {playblast_output_path}. It may be open in another application.")
                    return

        # プレイブラスト実行
        cmds.playblast(**playblast_options)

        # プレイブラスト後に元の表示設定に戻す
        if self.widget.polygon_checkBox.isChecked():
            cmds.modelEditor(cmds.playblast(ae=True), edit=True, allObjects=True)

        debug("Playblast done. Path: " + playblast_output_path, 'info')

        # ffmpegでエンコード
        ffmpeg_path = ''
        if self.widget.ffmpegPath_Default_radioButton.isChecked():
            # userScript/ffmpeg.exe
            ffmpeg_path = cmds.internalVar(userScriptDir=True) + 'ffmpeg.exe'
        elif self.widget.ffmpegPath_Custome_radioButton.isChecked():
            ffmpeg_path = self.widget.ffmpegPath_lineEdit.text()

        ffmpeg_option = self.widget.ffmpegOption_textEdit.toPlainText()

        savePath = self.widget.savePath_lineEdit.text()
        if not os.path.isdir(savePath):
            os.makedirs(savePath)

        fileNmae = self.widget.fileName_lineEdit.text() + '.mp4'

        ffmpeg_command = f'"{ffmpeg_path}" -i "{playblast_output_path}" {ffmpeg_option} "{savePath}/{fileNmae}"'
        process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # ffmpegの出力を表示
        for line in iter(process.stdout.readline, ''):
            if line:
                debug(f'ffmpeg output: {line.strip()}', 'debug')

        process.stdout.close()
        process.wait()  

        if process.returncode != 0:
            error_message = f'ffmpeg error: {process.returncode}'
            debug(error_message, 'error')
            QtWidgets.QMessageBox.critical(self, "Error", error_message)
            cmds.error(error_message)
        else:
            debug(f'ffmpeg done. Path: {savePath}/{fileNmae}', 'info')

            # プレイブラスト後のファイルを削除
            if self.widget.autoDelete_checkBox.isChecked():
                os.remove(playblast_output_path)
                debug(f'Playblast file deleted: {playblast_output_path}', 'info')

            # ファイルを開く
            if self.widget.openFile_checkBox.isChecked():
                os.startfile(f'{savePath}/{fileNmae}')

            # フォルダを開く
            if self.widget.openFolder_checkBox.isChecked():
                os.startfile(savePath)



        debug("Exiting export_playblast", 'trace')

def debug(log, level):
    # if level == 'trace':
    #     print('[playblast-ffmpeg] [TRACE]: '+log)
    # if level == 'debug':
    #     print('[playblast-ffmpeg] [DEBUG]: '+log)
    if level == 'info':
        print('[playblast-ffmpeg] [INFO]: '+log)
    if level == 'error':
        print('[playblast-ffmpeg] [ERROR]: '+log)

debug('loaded playblast_ffmpeg.py', 'info')

# how to use
# import playblast_ffmpeg
# playblast_ffmpeg.showUI()

# showUI()
