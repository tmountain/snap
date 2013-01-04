import lib.menu
import lib.term
import lib.box
import lib.rsync
import lib.ssh
import os
import subprocess

def main():
    menu = {
            "Snap to a node group": snap_group,
            "Snap to a node":snap_node,
            "Snap to testing node": snap_testing
           }

    lib.menu.navigate("Choose action",menu)()
    
    done_menu = {
                    "Return to main menu": "r",
                    "Exit":                "e"
                }
    next_action = lib.menu.navigate("Snap done, what do?",done_menu,clear_before=False)
    if next_action == "r":
        main()
    else:
        pass

def snap_group():
    group = lib.menu.navigate("Choose group to snap to",lib.box.groups,depth=0)
    snap_project(group)

def snap_node():
    node = lib.menu.navigate("Choose node to snap to",lib.box.nodes,depth=0)
    snap_project([node])

def snap_testing():
    node = lib.box.getNode("testy")
    snap_project([node])

def snap_project(destinations):
    project = lib.menu.navigate("Choose project",lib.box.projects)
    branch  = project.choose_and_checkout_branch()
    manifest = project.get_manifest()

    lib.term.clear()
    lib.menu.project_check(project)

    for (command,payload) in manifest:
        print()
        if command == "stage":
            do_stage(project,payload,destinations)
        elif command == "local-script":
            do_local_script(project,payload)
        elif command == "remote-script":
            do_remote_script(project,payload,destinations)

def do_stage(project,stages,destinations):
    for node in destinations:
        for stage in stages:
            lib.menu.header("Snapping {0} to {1}".format(stage,node["name"]))
            lib.rsync.rsync(project,node,stage)

def do_local_script(project,script):
    lib.menu.header("Running {0} locally".format(script))
    return project.snap_script(script)

def do_remote_script(project,script,destinations):
    for node in destinations:
        lib.menu.header("Running {0} script on {1}".format(script,node["name"]))
        return lib.ssh.ssh_project(node,"chmod +x snap/{0} && snap/{0}".format(script),project)

#Run when everything is set up
main()
