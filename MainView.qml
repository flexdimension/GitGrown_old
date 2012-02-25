import Qt 4.7

Rectangle {
    width: 1000
    height: 600
    BranchFlowView { id: bfView
        x:0
        y:0
    }

    StatusView{
        anchors.left: bfView.right
    }
}
