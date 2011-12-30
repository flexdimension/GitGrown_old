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

                Column {
                    Repeater {
                        model: parseInt(maxOffset) + (merge == "True" ? 0 : 1)
                        Image {
                            source: "images/to_parent.svg"
                            width: 50
                            height: 30
                        }
                    }
                }

                Image {
                    //anchors.horizontalCenter: parent.horizontalCenter
                    //y : parseInt(maxOffset) * 30
                    y: parseInt(maxOffset) * 30
                    source : "images/merge.svg"
                    width: 50
                    height: 30
                    visible: merge == "True"
                }

                Rectangle { id: maxOffsetObj
                    y: parseInt(maxOffset) * 30
                    height: 30
                    width: 30
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#EEAAAA"
                    radius: 10
                    opacity: 0.8
                }
                /*
                ImageLine {
                    property int diffIdx: idx_parent0 - index

                    x : 0
                    y : commitObj.y + commitObj.height / 2

                    x2 : 50
                    y2 : y
                    z : 0
                }
                */



                Rectangle { id: commitObj
                    y: parseInt(offset) * 30
                    height: 30
                    width: 30
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#DDDD60"
                    radius: 10
                    border.width:3
                    border.color:"#505020"

                    Text { id: indexText
                        text: index
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
                        text: summary.substring(0, 5) == 'Merge' ? summary : ''
                        font.pixelSize: 9
                        font.family:"Courier"
                        rotation: 30
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
            //Component.onCompleted: listView.positionViewAtEnd()
        }
    }
}
