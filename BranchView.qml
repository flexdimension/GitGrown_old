import Qt 4.7

Rectangle {
    width:400
    height:400

    color: "#AADDDD"

    property alias currentIndex: listView.currentIndex

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        Component { id: commitDelegate
            Rectangle { id: commitRect
                width: 50
                height: 400
                border.width: 1
                border.color: "#EEEEEE"
                color: "#DDDDDD"
                z: -10

                Rectangle { id: commitObj
                    y: parseInt(offset) * 30
                    height: 30
                    width: 30
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#DDDD60"
                    radius: 10

                    Text { id: indexText
                        text: listView.count - index - 1
                        font.pixelSize: 10
                        font.family:"Courier"
                    }

                    Text { id: authoredDateText
                        text: offset
                        font.pixelSize: 10
                        font.family:"Courier"
                        anchors.bottom: commitObj.bottom
                    }

                    Text { id: hexshaText
                        anchors.top: parent.bottom
                        text: hexsha.substring(0, 4) + '\n' + idx_parent0 + '\n' + idx_parent1
                        font.pixelSize: 10
                        font.family:"Courier"
                    }

                    Text { id: summaryText
                        anchors.top: hexshaText.bottom
                        text: summary.substring(0, 40)
                        font.pixelSize: 9
                        font.family:"Courier"
                        rotation: 45
                        transformOrigin:Item.TopLeft
                        z: 10
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
                        property int diffIdx: idx_parent0 - (listView.count - index - 1)

                        x : 0
                        y : parent.height / 2

                        x2 : -50 * diffIdx + 25
                        y2 : parent.height / 2
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
