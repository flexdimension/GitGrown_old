import Qt 4.7

Rectangle {
    width:400
    height:600

    color: "#AADDDD"

    property alias currentIndex: listView.currentIndex

    BranchListView {
        x: 0
        y: 0
        width: parent.width
        height: 200
    }

    Rectangle {
        x: 0
        y: 200
        width: parent.width
        height: 400
        anchors.margins: 10
        clip: true

        Component { id: commitDelegate
            Rectangle { id: commitRect
                width: 50
                height: 50
                border.width: 1
                border.color: "#EEEEEE"
                color: "#DDDDDD"
                z: -10
                Rectangle { id: commitObj
                    x: offset * 30
                    height: 30
                    width: 30
                    //anchors.horizontalCenter: parent.horizontalCenter
                    color: "#DDDD60"
                    radius: 10
                    border.width:3
                    border.color:"#909040"

                    Text { id: indexText
                        text: offset
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.pixelSize: 10
                        font.family:"Courier"
                    }
/*
                    Text { id: authoredDateText
                        text: offset
                        font.pixelSize: 10
                        font.family:"Courier"
                        anchors.bottom: commitObj.bottom
                    }

                    Text { id: hexshaText
                        anchors.left: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        text: hexsha.substring(0, 4) + '\n' + idx_parent0 + '\n' + idx_parent1
                        font.pixelSize: 10
                        font.family:"Courier"
                    }
*/
                    Text { id: summaryText
                        anchors.left: parent.right
                        //text: summary.substring(0, 5) == 'Merge' ? summary : ''
                        text: summary
                        font.pixelSize: 9
                        font.family:"Courier"
                        //rotation: 30
                        transformOrigin:Item.TopLeft
                        z: 10
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
            model: flowModel
            delegate: commitDelegate
            orientation: ListView.Vertical
            //layoutDirection:Qt.RightToLeft

            //layoutDirection: Qt.RightToLeft
            highlight: Rectangle {
                    color: "lightblue"
                    height: listView.currentItem.height
                    width: listView.width
                }
            //Component.onCompleted: listView.positionViewAtEnd()
        }
    }
}
