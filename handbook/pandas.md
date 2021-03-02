# Pandas V1.2.2

> import pandas as pd

## 输入
### 常用：
#### pd.read_csv()

参数：
1. header: 
2. names:
3. index_col: 

#### pd.read_sql(sql)

参数：
1. con: 
2. index_col: 

## 常用函数
### 拼接
#### pd.merge(left, right)

数据库风格拼接
参数：
1. how: {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘inner’
    - left: 只用left keys，类似sql中left outer join
    - right: 只用right keys，类似sql中right outer join
    - outer: 使用联合keys，类似sql中outer join
    - inner: 使用交集keys，类似sql中inner join
    - cross: 
2. index_col: 

可拼接df或series

pd.merge(left=df1, right=df2) == df1.merge(df2)

#### df.join(other)

列连接，连接效率高，默认NAN填充
参数：
1. on: str, list of str, or array-like
    - 连接key，默认使用索引
1. how: {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘inner’
    - left: 只用left keys，类似sql中left outer join
    - right: 只用right keys，类似sql中right outer join
    - outer: 使用联合keys，类似sql中outer join
    - inner: 使用交集keys，类似sql中inner join
    - cross: 
    
#### pd.concat(objs)
