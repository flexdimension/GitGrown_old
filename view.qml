import Qt 4.7
 

Rectangle {
    width: 1000
    height: 600

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

