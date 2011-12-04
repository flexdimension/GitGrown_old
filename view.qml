import Qt 4.7
 

Rectangle {
    width: 200
    height: 400

     Component {
         id: nameDelegate
         Text {
             text: name + " " + num
             font.pixelSize: 24
             anchors.left: parent.left
             anchors.leftMargin: 2
         }
     }

    ListView {
         anchors.fill: parent
         model: model2
         delegate: nameDelegate
         focus: true
         highlight: Rectangle {
             color: "lightblue"
             width: parent.width
         }

     }

}

