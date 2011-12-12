import Qt 4.7

Rectangle { id: blameView
    width:400
    height:400

    color: "#DDDDDD"

    property string currentCommit: ""

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        Component { id: fileViewDelegate

            Rectangle { id: lineBox
                width: parent.width
                height: codeText.height
                border.width: 1
                border.color: "#EEEEEE"
                color: "#DDDDDD"
                property bool isCurrent: blameView.currentCommit.substr(0, 8) == commit

                Rectangle { id: commitBox
                    anchors.left:parent.left
                    anchors.leftMargin:5
                    width: 60
                    height: commitText.height
                    radius: 4
                    border.width: 1
                    border.color: "#FFEEEE"
                    color: lineBox.isCurrent ? "#88FF88" : "#FFEEEE"

                    Text { id: commitText
                        anchors.left:parent.left
                        anchors.leftMargin:5
                        text: commit
                        font.pixelSize: 10
                        font.family:"Courier"
                    }
                }

                Rectangle { id: codeBox
                    anchors.left:commitBox.right
                    anchors.leftMargin:10
                    anchors.right: parent.right
                    height: codeText.height
                    color: lineBox.isCurrent ? "#DDFFDD" : "white"

                    Text { id: codeText
                        text: num + ") " + code
                        font.pixelSize: 10
                        font.family:"Courier"
                    }
                }
            }
        }

        ListView { id: listView
            anchors.fill: parent
            model: fileViewModel
            delegate: fileViewDelegate

            Rectangle {
                width: empty.width
                height: empty.height
                color: "#AAAAAA"
                visible: listView.count == 0 && listView.model != null

                Text { id: empty
                    text: "(empty)"
                    font.pixelSize: 10
                    font.family:"Courier"
                }
            }
        }
    }
}
