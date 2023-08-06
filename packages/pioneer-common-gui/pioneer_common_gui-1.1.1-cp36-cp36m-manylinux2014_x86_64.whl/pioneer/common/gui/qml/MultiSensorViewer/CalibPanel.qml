import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.11
import Leddar 1.0

Column
{
    id: component
    property var live
    GridLayout
    {
        columns: 6    
        Label
        {
            text: 'Wall distance:'
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: wallDistance_
            text: '2.0'
            validator: DoubleValidator
            {
                bottom: 1.5
                top: 10.0
            }
            selectByMouse: true
        }
        Label
        {
            text: 'Number of samples:'
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: number_samples_
            text: '100'
            validator: IntValidator
            {
                bottom: 5
                top: 500
            }
            selectByMouse: true
        }
        Label
        {
            text: 'Interpolate while calib.:'
            Layout.alignment: Qt.AlignRight
        }
        CheckBox
        {
            checked: component.live.interpCal
            onCheckedChanged: component.live.interpCal = checked
            Binding on checked
            {
                delayed: true
                value: component.live.interpCal
            }
        }
        Label
        {
            text: 'Correction of dist. with T.:'
            Layout.alignment: Qt.AlignRight
        }
        CheckBox
        {
            checked: component.live.dTCorrection
            onCheckedChanged: component.live.dTCorrection = checked
            Binding on checked
            {
                delayed: true
                value: component.live.dTCorrection
            }
        }
        Label
        {
            text: 'Gain factor:'
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: alphaT_
            text: component.live.dTGainFactor
            validator: DoubleValidator
            {
                bottom: 0.0
                top: 1.0
            }
            enabled: component.live.dTCorrection
            selectByMouse: true
            onEditingFinished:
            {
                component.live.dTGainFactor = alphaT_.text

            }
            Binding on text
            {
                delayed: true
                value: component.live.dTGainFactor
            }
        }
        Label
        {
            text: 'Base temperature:'
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: dTFix_
            text: component.live.dTFix
            validator: DoubleValidator
            {
                bottom: -10.0
                top: 60.0
            }
            enabled: component.live.dTCorrection
            selectByMouse: true
            onEditingFinished:
            {
                component.live.dTFix = dTFix_.text

            }
            Binding on text
            {
                delayed: true
                value: component.live.dTFix
            }
        }
            
      
          
        Label
        {
            text: 'Correction of ampl. with T.:'
            Layout.alignment: Qt.AlignRight
        }
        CheckBox
        {
            checked: component.live.aTCorrection
            onCheckedChanged: component.live.aTCorrection = checked
            Binding on checked
            {
                delayed: true
                value: component.live.aTCorrection
            }
        }
        Label
        {
            text: 'Gain factor:'
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: gammaT_
            text: component.live.aTGainFactor
            validator: DoubleValidator
            {
                bottom: 0.0
                top: 100.0
            }
            enabled: component.live.aTCorrection
            selectByMouse: true
            onEditingFinished:
            {
                component.live.aTGainFactor = gammaT_.text
            }
            Binding on text
            {
                delayed: true
                value: component.live.aTGainFactor
            }
        }
        Label
        {
            text: 'When T >'
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: gammaTThreshold_
            text: component.live.aTThreshold
            validator: DoubleValidator
            {
                bottom: 0.0
                top: 100.0
            }
            enabled: component.live.aTCorrection
            selectByMouse: true
            onEditingFinished:
            {
                component.live.aTThreshold = gammaTThreshold_.text
            }
            Binding on text
            {
                delayed: true
                value: component.live.aTThreshold
            }
        }
        Label
        {
            text: 'Resolution specs:'
            Layout.alignment: Qt.AlignRight
        }
        ComboBox
        {
            height: 25
            textRole: "key"
            model: ListModel 
            {
                id: modelfov
                ListElement { key: "NONE" }
                ListElement { key: "v_fov" }
                ListElement { key: "h_fov" }
                ListElement { key: "v" }
                ListElement { key: "h" }

            }
            currentIndex: 0
            onActivated:
            {
                component.live.editResoSpecs(modelfov.get(currentIndex).key)
            }
        }
        Label
        {
            text: 'Value: '
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: resovaluespecs_
            text: component.live.resoSpecsVal
            validator: DoubleValidator
            {
                bottom: 0.0
                top: 1000.0
            }
            enabled: component.live.editingResoSpecs
            selectByMouse: true
            onEditingFinished:
            {
                component.live.changeResoSpecs(parseFloat(resovaluespecs_.text))
            }
            Binding on text
            {
                delayed: true
                value: component.live.resoSpecsVal
            }
        }
        Label
        {
            text: ' '
        }
        Label
        {
            text: ' '
        }
        
        Label
        {
            text: 'Custom v angles:'
            Layout.alignment: Qt.AlignRight
        }
        CheckBox
        {
            checked: component.live.vtabanglesCorrection
            onCheckedChanged: component.live.vtabanglesCorrection = checked
            Binding on checked
            {
                delayed: true
                value: component.live.vtabanglesCorrection
            }
        }
        Label
        {
            text: 'File:'
            Layout.alignment: Qt.AlignRight
        }
        ComboBox
        {
            id: fileanglestable_
            height: 25
            implicitWidth:  200
            model: component.live.listFilesCustomVAngles
            enabled: component.live.vtabanglesCorrection
        }

        Label
        {
            text: 'Scaling:'
            Layout.alignment: Qt.AlignRight
        }
        TextField
        {
            id: vanglescaling_
            text: component.live.scalevangles
            validator: DoubleValidator
            {
                bottom: 0.0
                top: 100.0
            }
            enabled: component.live.vtabanglesCorrection
            selectByMouse: true
            onEditingFinished:
            {
                component.live.scalevangles = vanglescaling_.text
            }
            Binding on text
            {
                delayed: true
                value: component.live.scalevangles
            }
        }

        Label
        {
            text: ' '
        }
        
        Button
        {
            text: "Apply \!"
            onClicked: component.live.changeAnglesSpecs(fileanglestable_.currentText)
            enabled: component.live.vtabanglesCorrection
        }

        Label
        {
            text: ' '
        }
        Label
        {
            text: ' '
        }
        Label
        {
            text: ' '
        }
        Label
        {
            text: ' '
        }

        
        Button
        {
            text: (component.live.restoringCal ? "Restored" : "Restore calibration \\!/")
            onClicked: component.live.restoreCalibration("rcalibration/"+spath2rcal_.text)
            enabled: !component.live.restoringCal
        }
        Label
        {
            text: ' '
        }
        Label
        {
            text: 'File:'
            Layout.alignment: Qt.AlignRight
        }

        ComboBox
        {
            height: 25
            implicitWidth:  200
            model: component.live.listFilesRCal
            enabled: true
        }

        Label
        {
            text: ' '
        }
        Label
        {
            text: ' '
        }


        Button
        {
            text: (component.live.calibrating ? ("calibrating : " + (component.live.calibrationProgress * 100).toFixed(1) + " %") : "calibrate \\!/")
            onClicked: component.live.calibrate(parseFloat(wallDistance_.text), parseInt(number_samples_.text))
            enabled: !component.live.calibrating
        }
        Label
        {
            text: ' '
        }


        Label
        {
            text: 'Saving into:'
            Layout.alignment: Qt.AlignRight
        }
        
        TextField
        {
            id: spath2rcal_
            text: component.live.savingcalibinto
            selectByMouse: true
            enabled: !component.live.calibrating
            onEditingFinished:
            {
                component.live.savingcalibinto = spath2rcal_.text
            }
            Binding on text
            {
                delayed: true
                value: component.live.savingcalibinto
            }
        }

        
        
    }
        
}
