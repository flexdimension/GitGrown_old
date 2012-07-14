import Qt 4.7

Rectangle {
        width:400
        height:300

        color: "#AADDDD"
        Row {
            Repeater {
                model: 10
                Rectangle {
                    width: 50
                    height: 200
                    border.color: "#DDDDDD"
                    color: "transparent"
                }
            }
        }

        Rectangle{
            width: parent.width
            height: parent.height
            color: "transparent"
            Component { id:branchDelegate
                Rectangle { id: content
                    x: 0
                    width: 100
                    height: 20
                    color: "#AABBCC"
                    Text {
                        text: name
                    }

                    MouseArea {
                        anchors.fill: parent
                        drag.target: content
                        drag.axis: Drag.XAxis
                        drag.minimumX: 0
                        drag.maximumX: 300
                    }
                }


            }

            ListView {
                width: parent.width
                height: parent.width
                model: branchListModel
                delegate: branchDelegate
            }
        }




}
