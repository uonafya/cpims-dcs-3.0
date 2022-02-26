from fabric.api import local, lcd

def prepare_deployment(branch_name):
    local('python manage.py test myapp')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

def deploy():
    with lcd('/home/nmugaya/Repo/cpims/'):
        local('git pull /home/nmugaya/Projects/cpims/')
        '''
        local('python manage.py migrate myapp')
        local('python manage.py test myapp')
        local('/my/command/to/restart/webserver')
        '''

# fab prepare_deployment:dev
# fab deploy 
