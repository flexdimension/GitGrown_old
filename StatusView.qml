import Qt 4.7

Rectangle { id: statusView
    width:400
    height:600

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
            PushButton {
                width: 80
                height: 30
                text: "Refresh"
                objectName: "refreshButton"
                onClicked : {
                    console.log("refresh push button clicked!!")
                }
            }

            PushButton {
                width: 80
                height: 30
                text: "Commit"
                objectName: "commitButton"

                signal commitWithMessage(string msg)

                onClicked : {
                    commitWithMessage(textCommit.text)
                    console.log("commit push button clicked!!")
                }
            }

            Rectangle {
                width: parent.width
                height: 30
                border.color: "black"
                TextInput { id: textCommit
                    anchors.fill: parent
                    anchors.margins: 3
                }
            }
        }

        Rectangle { id: statusConsole
            width: parent.width
            anchors.top: statusController.bottom
            height: 300
            border.color:"gray"


            Text {
                id: statusText
                text: gitStatus
            }
        }

        ListView {
            anchors.top: statusConsole.bottom
            width: parent.width
            height: 300
            model: indexModel
            delegate: indexDelegate


            Component { id: indexDelegate
                Rectangle {
                    width: parent.width
                    height: 20
                    border.width: 1
                    border.color: "black"

                    Text {
                        text: name + ":" + type
                    }

                }
            }
        }
    }
}
