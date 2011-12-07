import Qt 4.7
 

Rectangle {
    width: 800
    height: 600


/*
     Component {
         id: nameDelegate
         Text {
             text: section + "=" + value
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
*/
    GitFileBrowser{ id: gfb
        objectName: "fileBrowser"

    }

    BlameView { id: bv
        objectName: "blameView"
        anchors.left: gfb.right
    }

    CommitListView { id: clv
        objectName: "commitListView"
        anchors.left:bv.left
        anchors.top:bv.bottom
    }
}

