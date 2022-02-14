# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'Tool'
__author__ = 'sudoskys'
__time__ = '2022/2/11 下午9:11'
__product_name__ = 'PyCharm'
__version__ = '2月112111'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""
import logging.config

class useTool(object):
    # github：sudoskys
    def __init__(self):
        self.debug = True
        import os
        self.home = os.getcwd()

    def dprint(self, log):
        """
        :param log: self print
        :return:
        """
        if self.debug:
            print(log)

    def remove(self, top):
        """
        :param top:
        :return:
        """
        import os
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def filesafer(self, filen):
        """
        :param filen:
        :return:
        """
        def wr(filen):
            import os
            file_dir = os.path.split(filen)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if not os.path.exists(filen):
                os.system(r'touch %s' % filen)
            return filen

        try:
            road = wr(filen)
            # droad = os.getcwd() + road
            self.dprint("New+ " + road)
            return road
        except IOError:
            import os
            print("重定向路径中" + str(os.getcwd() + '/' + filen))
            try:
                road = wr(os.getcwd() + '/' + filen)
                return road
            except IOError as err:
                print("err", err)
                print("Error:NOT FOUND FILE 没有找到文件或读取文件失败")
                return False
    def sData(self, file_name, tables):
        """
        :param file_name:
        :param tables:
        :return:
        """
        self.filesafer(file_name)
        if isinstance(tables, (dict, list)):
            try:
                from ruamel.yaml import YAML
                yaml = YAML()
                with open(file_name, 'w') as f_obj:
                    yaml.dump(tables, f_obj)
            except IOError as err:
                # mLog("err", err).wq()
                logging.error(err)
                raise Exception("NOT FOUND FILE 没有找到文件或读取文件失败", err)
            else:
                return True
        else:
            print("Type Error:MUST TABLE", tables)
            return False

    def rData(self, file_names):
        """
        :param file_names:
        :return:
        """
        import os
        file_name = os.getcwd() + '/' + file_names
        self.filesafer(file_name)
        with open(file_name) as f_obj:
            try:
                from ruamel.yaml import YAML
                data = YAML(typ='safe').load(f_obj)
                # print(data)
                return data
            except Exception as err:
                # mLog("err", err).wq()
                logging.error(err)
                return {}
