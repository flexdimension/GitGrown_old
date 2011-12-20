import Qt 4.7
 

Rectangle {
    width: 1000
    height: 600

    GitFileBrowser{ id: gfb
        objectName: "fileBrowser"

    }

    BlameView { id: bv
        objectName: "blameView"
        anchors.left: clv.right
    }

    CommitListView { id: clv
        objectName: "commitListView"
        anchors.left:gfb.right
        anchors.top:parent.top
    }

    BranchView { id: bgv
        objectName: "branchView"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top:gfb.bottom
        anchors.bottom: parent.bottom
    }
}

