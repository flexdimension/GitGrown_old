import Qt 4.7

Rectangle { id: root
    objectName: "root"

    width: 1000
    height: 600

    signal commited

    BranchFlowView { id: bfView
        x:0
        y:0
    }

    StatusView{
        anchors.left: bfView.right
    }
}
