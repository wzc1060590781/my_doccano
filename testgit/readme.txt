git init

git add file

git status

git commit -m "message"

git reset --hard Head^ 回退到上一个版本


命令 git checkout --readme.txt 意思就是，把readme.txt文件在工作区做的修改全部撤销，这里有2种情况，如下：

	readme.txt自动修改后，还没有放到暂存区，使用 撤销修改就回到和版本库一模一样的状态。
	另外一种是readme.txt已经放入暂存区了，接着又作了修改，撤销修改就回到添加暂存区后的状态。



只要没有commit之前，如果我想在版本库中恢复此文件如何操作呢？

　　可以使用如下命令 git checkout  -- b.txt，如下所示：


# 测试远程连接
ssh -T git@gitlab.706.com


# 添加远程仓库
git remote add origin https://github.com/wzc1060590781/706.git
