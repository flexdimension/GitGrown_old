import Qt 4.7

ListModel {
     id: nameModel
     ListElement { name: "Alice"; team: "Crypto" }
     ListElement { name: "Bob"; team: "Crypto" }
     ListElement { name: "Jane"; team: "QA" }
     ListElement { name: "Victor"; team: "QA" }
     ListElement { name: "Wendy"; team: "Graphics" }
 }
 Component {
     id: nameDelegate
     Text {
         text: name;
         font.pixelSize: 24
         anchors.left: parent.left
         anchors.leftMargin: 2
     }
 }
