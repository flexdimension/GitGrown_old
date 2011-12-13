'''
Created on 2011/12/12

@author: unseon_pro
'''

from GitModel import GitModel

if __name__ == '__main__':
    gm = GitModel()
    gm.connect('.')

    bi = dict()
    cnt = 0
    for b in gm.repo.heads :
        name = b.name
        for c in gm.repo.iter_commits(name) :
            date = c.authored_date
            sha = c.hexsha
            parents = []
            for p in c.parents :
                parents.append(p.hexsha)
            bi[sha] = [cnt, name, date, sha, parents]
        cnt += 1
            

        
    bbi = sorted(bi.items(), key = lambda x : x[1][2], reverse = True)
            
    for i in bbi :
        print i
            
    '''
    for i in sbi :
        if len(new_bi) == 0 or i[2] != new_bi[-1][3] :
            new_bi.append([1]+i)
            
    
    for i in new_bi :
        print i
        '''