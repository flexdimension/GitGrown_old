import Qt 4.7


Rectangle {
    width: 200
    height: 400
    border.width: 1
    color: "#00B000"


    Rectangle {

        anchors.fill: parent
        anchors.margins:10
        clip: true

        Component {
            id: fileDelegate
            Rectangle {
                width: parent.width
                height: textBox.height
                color: type == 'file' ? "#D0D0FF" : "#FFD0FF"
                radius: 4
                border.width: 1
                border.color: "#DDDDDD"

                Text { id : textBox
                    text: name
                    font.pixelSize: 12
                    font.family:"Courier"
                    anchors.left: parent.left
                    anchors.leftMargin: 10 + (path.split('/').length - 1) * 20
                }
            }
         }

        ListView {
             anchors.fill: parent
             model: fileListModel
             delegate: fileDelegate
             focus: true
             highlight: Rectangle {
                 color: "lightblue"
                 width: parent.width
             }

         }
    }
}
