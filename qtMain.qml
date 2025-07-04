import QtQuick
import QtQuick.Controls

Window{
    visible: true
    width: 400
    height: 300
    title: 'My QtQuick App'

    Rectangle{
        anchors.fill: parent
        color: 'white'
        Text {
            text:'Hello QtQuick from Python'
            anchors.centerIn: parent
        }
    }
}