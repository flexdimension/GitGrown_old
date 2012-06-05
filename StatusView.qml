import Qt 4.7

Rectangle { id: statusView
    width:300
    height:600

    color: "#DDDDDD"

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        width: parent.width
        Column {
            width: parent.width

            Rectangle { id: indexFrame
                width: parent.width
                height: 200

                property int indent: 40

                Rectangle { id: workingBox
                    x: 0
                    y: 0
                    width: parent.width - indexFrame.indent
                    height: indexView.count * 22 + 20 + 5
                    border.color: "black"
                    color: "white"
                }

                Rectangle { id: commitBox
                    x: indexFrame.indent
                    y: 20
                    width: parent.width - x
                    height: indexView.count * 22 + 10
                    radius: 10
                    color: "#EEF0AA"
                    border.color: "#77AA77"
                    border.width: 2
                }

                ListView { id: indexView
                    y: 25
                    width: parent.width
                    height: 300
                    model: indexModel
                    delegate: indexDelegate

                    clip: true
                    spacing: 2

                    objectName: "indexStatus"

                    signal stageFile(string path)
                    signal unstageFile(string path)
                    signal discardFile(string path)

                    Component { id: indexDelegate
                        Rectangle {
                            x : 10
                            width: parent.width - 20
                            height: 20
                            border.width: 1
                            border.color: "gray"
                            color: "transparent"

                            Rectangle { id: modifedFileBox
                                x: indexFrame.indent
                                width: parent.width / 2
                                height: 20
                                //Show only if file is modified and staged
                                visible: type.indexOf("M") != -1 || type.indexOf("R") != -1
                                border.width: 1
                                radius: 8


                                Text {
                                    x:0
                                    text: path + ":" + type
                                    color: "green"
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked : {
                                        console.log('unstage ' + path)
                                        indexView.unstageFile(path)
                                    }
                                }

                            }

                            Rectangle { id: changedFileBox
                                x: 0
                                width: parent.width / 2
                                height: 20
                                //Show only if the file is changed but not staged
                                visible: type.indexOf("C") != -1
                                border.width: 1
                                radius: 8

                                Text {
                                    x:0
                                    text: path + ":" + type
                                    color: "red"
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked : {
                                        console.log('stage ' + path)
                                        indexView.stageFile(path)
                                    }
                                }
                            }

                            Rectangle { id: newFileBox
                                x: indexFrame.indent
                                width: parent.width / 2
                                height: 20
                                //Show only if file is modified and staged
                                visible: type.indexOf("N") != -1
                                color: "#AADDAA"
                                border.width: 1
                                radius: 8

                                Text {
                                    x:0
                                    text: path + ":" + type
                                    color: "green"
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked : {
                                        console.log('unstage ' + path)
                                        indexView.unstageFile(path)
                                    }
                                }
                            }



                            Rectangle { id: untrackedFileBox
                                x: 0
                                width: parent.width / 2
                                height: 20
                                //Show only if the file is untracked
                                visible: type.indexOf("U") != -1
                                color: "#DDAAAA"
                                border.width: 1
                                radius: 8

                                Text {
                                    x:0
                                    text: path + ":" + type
                                    color: "red"
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked : {
                                        console.log('stage ' + path)
                                        indexView.stageFile(path)
                                    }
                                }
                            }

                        }
                    }
                }

            }



            Column { id: statusController
                width: parent.width

                Rectangle { id: title
                    width: parent.width
                    height: 40
                    Text {
                        text: "Status"
                    }
                }
                PushButton {
                    width: 80
                    height: 30
                    text: "Refresh"
                    objectName: "refreshButton"
                    onClicked : {
                        console.log("StatusView:" + "refresh push button clicked!!")
                    }
                }

                PushButton {
                    width: 80
                    height: 30
                    text: "Undo Commit"
                    objectName: "undoCommitButton"

                    signal undoCommit
                    onClicked : {
                        undoCommit()
                        console.log("StatusView:" + "Undo Commit push button clicked!!")
                    }
                }

                PushButton {
                    width: 80
                    height: 30
                    text: "Commit"
                    objectName: "commitButton"

                    signal commitWithMessage(string msg)

                    onClicked : {
                        commitWithMessage(commitMessage.text)
                        console.log("StatusView:" + "commit push button clicked!!")
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 60
                    border.color: "black"
                    TextEdit { id: commitMessage
                        objectName: "commitMessage"
                        anchors.fill: parent
                        anchors.margins: 3
                        wrapMode: TextEdit.Wrap

                        Component.onCompleted: {
                            root.commited.connect(clear)
                            root.commitUndone.connect(setMessage)
                        }

                        function clear() {
                            text = ""
                        }

                        function setMessage(msg) {
                            text = msg
                        }
                    }
                }
            }

        }
    }


}
