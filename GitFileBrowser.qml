import Qt 4.7


Rectangle {
    width: 200
    height: 400
    border.width: 1
    color: "#00B000"

    property alias currentIndex: listView.currentIndex


    Rectangle {

        anchors.fill: parent
        anchors.margins:10
        clip: true

        Component {
            id: fileDelegate

            Rectangle { id:box
                width: parent.width-20
                height: textBox.height + 5
                color: type == 'blob' ? "#D0D0FF" : "#FFD0FF"
                radius: 4
                border.width: 1
                border.color: "#DDDDDD"

                Text { id : textBox
                    text: name
                    font.pixelSize: 12
                    font.family:"Courier"
                    anchors.left: parent.left
                    anchors.leftMargin: index == 0 ? 0 : 10 + (path.split('/').length - 1) * 20
                }


                MouseArea {
                    anchors.fill: parent
                    onClicked : {
                        fileListModel.onSelected("path", path)
                        listView.currentIndex = index
                    }
                }
            }

         }

        ListView { id: listView
             anchors.fill: parent
             model: fileListModel
             delegate: fileDelegate
             focus: true
             //highlightFollowsCurrentItem: true
             highlight: Rectangle {
                 color: "lightblue"
                 height: parent.height
                 width: parent.width
             }

         }
    }
}
