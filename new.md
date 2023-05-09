### 测试gitbash

1. **设置用户**

    `git config --global user.name "Meng_Ren"`

    `git config --global user.email  "3029606296@qq.com"`

2. **进入文件夹**

    `cd ./Documents/`
    
    `cd ./code/`

    `pwd`
    
    /c/Users/30296/Documents/code
    
    `ls`

3. **创建文件夹**

    `mkdir front-end`
    
    `cd front-end/`
4. **初始化**

   `git init`

   Initialized empty Git repository in C:/Users/30296/Documents/code/front-end/.git/
5. **远程**

   `git remote add renmeng git@github.com:Mousikar/machine-vision.git`

   `git remote add renmeng git@github.com:Mousikar/machine-vision.git`
   
   error: remote renmeng already exists.
   
   `git remote -v`

   renmeng git@github.com:Mousikar/machine-vision.git (fetch)
   renmeng git@github.com:Mousikar/machine-vision.git (push)
6. **新建文件**

   `touch new.md`

7. **提交文件**

   `git add -A`
   
   `git commit -m "测试gitbash"`

   `git push -u renmeng master`

### 解决报错：
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.


1. 生成新的SSH key

   `ssh-keygen -t rsa -C "3029606296@qq.com"`

2. 将SSH key 添加到 ssh-agent

   `eval "$(ssh-agent -s)"`

   Agent pid 1196

   `ssh-add ~/.ssh/id_rsa`

   Identity added: /c/Users/30296/.ssh/id_rsa (3029606296@qq.com)

3. 将SSH key添加到GitHub账户

   在账户选项中选择 “Settings”–>“SSH and GPG keys”–>“New SSH key”，然后打开之前新生成的id_rsa.pub文件，将密钥复制后填写到账户中【注意填写时的格式要求】

4. 验证key

   `ssh -T git@github.com`

   Hi Mousikar! You've successfully authenticated, but GitHub does not provide shell access.
