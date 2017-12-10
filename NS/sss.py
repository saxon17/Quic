
def dfs(self, A, k, target, index, onelist):

        if (target == 0 and k == 0):
            self.anslist.append(onelist)
            return None
        if (len(A) == index or target < 0 or k < 0):
            return None
        self.dfs(A, k, target, index + 1, onelist)
        otheronelist = [A[index]]
        otheronelist.extend(onelist)
        self.dfs(A, k - 1, target - A[index], index + 1, otheronelist)

def kSumII(self, A, k, target):
        self.anslist = []
        self.dfs(A, k, target, 0, [])
        return self.anslist
KS