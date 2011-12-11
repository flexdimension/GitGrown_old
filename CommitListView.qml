import Qt 4.7

Rectangle {
    width:600
    height:200

    color: "#AADDDD"

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        Component { id: commitListDelegate
            Rectangle {
                width: parent.width -20
                height: hexshaBox.height
                border.width: 1
                border.color: "#EEEEEE"
                color: "#DDDDDD"

                Rectangle { id: hexshaBox
                    anchors.left:parent.left
                    anchors.leftMargin:5
                    width: 250
                    height: hexshaText.height
                    radius: 4
                    border.width: 1
                    border.color: "#FFEEEE"
                    color: "#FFEEEE"

                    Text { id: hexshaText
                        anchors.left:parent.left
                        anchors.leftMargin:5
                        text: hexsha
                        font.pixelSize: 10
                        font.family:"Courier"
                    }
                }

                Rectangle { id: authoredDateBox
                    anchors.left:hexshaBox.right
                    anchors.leftMargin:10
                    anchors.right: parent.right
                    height: authoredDateText.height

                    Text { id: authoredDateText
                        text: author_name + " " + authored_date
                        font.pixelSize: 10
                        font.family:"Courier"
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked : {
                        commitListModel.onSelected("hexsha", hexsha)
                        listView.currentIndex = index
                    }
                }
            }
        }

        ListView { id: listView
            anchors.fill: parent
            model: commitListModel
            delegate: commitListDelegate
            highlight: Rectangle {
                    color: "lightblue"
                    height: listView.currentItem.height
                    width: listView.width
                }
        }
    }
}
