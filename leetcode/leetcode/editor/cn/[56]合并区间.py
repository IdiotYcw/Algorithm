# 以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi] 。请你合并所有重叠的区间，并返
# 回一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
# 输出：[[1,6],[8,10],[15,18]]
# 解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
#  
# 
#  示例 2： 
# 
#  
# 输入：intervals = [[1,4],[4,5]]
# 输出：[[1,5]]
# 解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= intervals.length <= 104 
#  intervals[i].length == 2 
#  0 <= starti <= endi <= 104 
#  
#  Related Topics 排序 数组 
#  👍 821 👎 0


# leetcode submit region begin(Prohibit modification and deletion)
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) == 1:
            return intervals
        intervals = sorted(intervals, key=lambda x: x[0])
        results = []
        start = intervals[0]
        for inter in intervals[1:]:
            if inter[0] > start[1]:
                results.append(start[:])
                start = inter
            else:
                start = [start[0], max(start[1], inter[1])]

        if inter[0] > start[1]:
            start = inter
        else:
            start = [start[0], max(start[1], inter[1])]
        results.append(start[:])

        return results
# leetcode submit region end(Prohibit modification and deletion)
