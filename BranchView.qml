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
                        model: decor.length



                        Image {
                            source: decorToFileName(decor.substr(index, 1))
                            width: 50
                            height: 30
                            function decorToFileName(d) {
                                switch(d) {
                                case '\\':
                                    return 'images/merge.svg'
                                case '/':
                                    return 'images/branch.svg'
                                case 'v':
                                    return 'images/forward_merge.svg'
                                case '|':
                                case '*':
                                    return 'images/forward.svg'
                                default:
                                    return ''
                                }
                            }
                        }
                    }
                }

                Rectangle { id: feedLine
                    anchors.horizontalCenter: parent.horizontalCenter
                    y: (commitOffset(decor) + 1) * 30
                    color: "#2222FF"

                    width: 10
                    height: (maxFeed(decor) - commitOffset(decor) -1) * 30
                    function maxFeed(d) {
                        for(var i = d.length - 1; i >= 0; i--) {
                            if("\\/<*".indexOf(d.charAt(i)) != -1)
                                break;
                        }
                        return i
                    }

                    function commitOffset(d) {
                        return d.indexOf('*');
                    }

                }

                Rectangle { id: maxOffsetObj
                    y: parseInt(maxOffset) * 30
                    height: 30
                    width: 30
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#EEAAAA"
                    radius: 10
                    opacity: 0
                }

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
