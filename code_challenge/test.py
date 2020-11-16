from code_challenge.github_get import GitApi
if __name__ == '__main__':
    print('Question - 2')
    git_repo = GitApi(url='https://api.github.com/users/', owner='SeleniumHQ',
                      access_token='5f0d671bdf8aaddb8760a136adc93133a4f31951')

    # answer point a
    print('a. Total open issues across all repositories are %s' % git_repo.get_total_issue())
    # answer b. Sort the repositories by date updated in descending order.
    print('b. Sort the repositories by date updated in descending order.')

    print(git_repo.get_sorted_lst())
    print('Note b. There is an issue that the updated date returned by api does not match with one on '
          'https://github.com/SeleniumHQ or it different')

    # answer c
    print('c. The most watchers repository is %s' % git_repo.get_most_watcher_repo())


