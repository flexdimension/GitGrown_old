import Qt 4.7

Rectangle {
    width:400
    height:200

    color: "#AADDDD"

    property alias currentIndex: listView.currentIndex

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        Component { id: commitDelegate
            Rectangle { id: commitRect
                width: 50
                height: 200
                border.width: 1
                border.color: "#EEEEEE"
                color: "#DDDDDD"

                Rectangle { id: commitObj
                    y: parseInt(offset) * 30
                    height: 30
                    width: 30
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#DDDD60"
                    radius: 10

                    Text { id: authoredDateText
                        text: offset
                        font.pixelSize: 10
                        font.family:"Courier"
                    }


                    /*
                    Image {
                        source: "images/line.svg"
                        anchors.right: commitObj.horizontalCenter
                        anchors.verticalCenter: commitObj.verticalCenter
                        height: 5
                        width: commitRect.width
                    }
                    */


                    ImageLine {
                        x : parent.width / 2
                        y : parent.height / 2

                        x2 : -50
                        y2 : parent.height / 2 + 50
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
            model: branchGraphModel
            delegate: commitDelegate
            orientation: ListView.Horizontal
            //layoutDirection:Qt.RightToLeft

            //layoutDirection: Qt.RightToLeft
            highlight: Rectangle {
                    color: "lightblue"
                    height: listView.currentItem.height
                    width: listView.width
                }
            Component.onCompleted: listView.positionViewAtEnd()
        }
    }
}
