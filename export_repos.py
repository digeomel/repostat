import sys
import os
import shutil
import gitstats


def usage():
    print('cli usafe:  export_repos.py [root] [output folder]')
    print('Export git repos!')
    print('Expected root folder structure:')
    print('root -> contain the projects')
    print('   |- project -> contain the repos of the project')
    print('      |-  gitrepo -> git repo')
    print('')
    print('Result generated in output folder as source folders structured')
    print('project folder name will be the project_name option in getstats cli command')

for a in sys.argv[1:]:
    print("Args: " + a)

if (len(sys.argv) != 3):
    usage()
    sys.exit(1)

project_folder = sys.argv[1]
output_folder = sys.argv[2]
tmp_output = os.path.join(output_folder, 'tmp')

def move_csv(target):
    files = os.listdir(tmp_output)

    for f in files:
        shutil.move(os.path.join(tmp_output, f), target)

print("Project folder: " + project_folder)
print("Output folder: " + output_folder)

#delete output dir
try:
    shutil.rmtree(output_folder)
except OSError:
    pass
os.makedirs(tmp_output)
base_path = project_folder
for d in os.listdir(base_path):
    abs_dir = os.path.join(base_path, d)

    if os.path.isdir(abs_dir):
        for gd in os.listdir(abs_dir):
            abs_gdir = os.path.join(abs_dir, gd)
            if os.path.isdir(abs_gdir):
                #create target folder
                target_dir = os.path.join(output_folder, d, gd)
                os.makedirs(target_dir)
                #call generator export to tmp folder
                g = gitstats.GitStats()
                g.run(['-coutput=csv', format("-cproject_name=%s" % d), abs_gdir + ' ', tmp_output + ' '])
                #move result csv from tmp folder to target dir
                move_csv(target_dir)
                #shutil.move(os.path.join(tmp_output, "*.csv"), os.path.join(target_dir, "*.csv"))

try:
    shutil.rmtree(tmp_output)
except OSError:
    pass
