# system
import os


#####################################################
# just a boilerPlate for the apk/app bundle release #
#####################################################


# will run the command which will create the binary (apk/app bundle)
def release_binary(release_command, project_path, gradle_path):
    cd_command = f'cd {project_path}'
    if gradle_path is None:
        gradle_path = os.path.join('.', 'gradlew')
    gradle_command = f'{gradle_path} {release_command}'
    full_command = f'{cd_command} && {gradle_command}'
    os.system(full_command)
