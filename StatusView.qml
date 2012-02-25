import Qt 4.7

Rectangle { id: statusView
    width:400
    height:400

    color: "#DDDDDD"

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        Column { id: statusController
            width: parent.width

            Rectangle { id: title
                width: parent.width
                height: 40
                Text {
                    text: "Status"
                }
            }
            Rectangle { id: refreshButton
                border.width:1
                border.color: 'black'
                width: parent.width
                height: 40

                Text {
                    text: "Refresh"
                }
                MouseArea {
                    anchors.fill: parent
                    objectName: "refreshButton"
                }
            }
        }

        Rectangle {
            width: parent.width
            anchors.top: statusController.bottom
            anchors.bottom: parent.bottom


            Text {
                id: statusText
                text: gitStatus
            }
        }

    }
}
