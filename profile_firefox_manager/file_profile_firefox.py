from os import mkdir, getenv
from os.path import isdir, isfile, dirname, exists
import json
import configparser

from profile_firefox_manager.archive import folder_to_archive, archive_to_folder


class ProfileFirefoxConfig:

    def __init__(self, index: int, name: str, path: str):
        if name == "" or path == "":
            raise Exception("Name or Path empty")

        self.old_index = index
        self.old_name = name
        self.old_path = path
        self.index = self.old_index
        self.name = self.old_name
        self.path = self.old_path

    def __str__(self):
        return "Index: {0}\nName: {1}\nPath: {2}\nSelected: {3}\n".format(self.index, self.name, self.path,self.selected)

    def __eq__(self, other):
        if (self.old_index == other.old_index
            and self.old_name == other.old_name
                and self.old_path == other.old_path):

            return True
        else:
            return False


class ProfileFirefoxConfigHandler(ProfileFirefoxConfig):

    def __init__(self, index: int = -1, name: str = "", path: str = "", work_folder: str = "", path_fpk: str = ""):
        if path_fpk != "":
            self._path_fpk = path_fpk
            index = -1
            name, path = self._read_fkg()
            pass
        super().__init__(index, name, path)

        self.work_folder = work_folder
        if self.work_folder[-1] != "/":
            self.work_folder += "/"
        self.selected = False

    def _read_fkg(self):
        with open(self._path_fpk) as f:
            manifest = json.load(f)
            return manifest["name"], manifest["path"]

    def from_pack(self):
        archive_to_folder(dirname(self._path_fpk) + "/" + self.old_name + ".zip",
                          dirname(self.work_folder + self.old_path))

    def from_pack_check(self):
        if not isdir(self.work_folder):
            return False
        if isdir(self.work_folder + "/" + self.old_path):
            return False
        if not isfile(dirname(self._path_fpk) + "/" + self.old_name + ".zip"):
            return False
        return True

    def to_pack(self, path_pack: str):
        t_path_manifest = path_pack + ".fpk"
        t_path_archive = dirname(path_pack) + "/" + self.name + ".zip"
        print(t_path_archive)
        if exists(t_path_manifest) or exists(t_path_archive):
            raise Exception("Error exists package ")

        manifest = {
            "name": self.name,
            "path": self.path
        }
        with open(t_path_manifest, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=4)

        folder_to_archive(t_path_archive, self.get_full_path())

    def get_full_path(self):
        return self.work_folder + self.path

    def enable_proxy(self, proxy_ip: str, proxy_port: int):

        proxy_ip = '"' + proxy_ip + '"'
        t_settings_new = [
                ("network.proxy.backup.ftp", proxy_ip),
                ("network.proxy.backup.ftp_port", proxy_port),
                ("network.proxy.backup.ssl", proxy_ip),
                ("network.proxy.backup.ssl_port", proxy_port),
                ("network.proxy.ftp", proxy_ip),
                ("network.proxy.ftp_port", proxy_port),
                ("network.proxy.http", proxy_ip),
                ("network.proxy.http_port", proxy_port),
                ("network.proxy.share_proxy_settings", "true"),
                ("network.proxy.ssl", proxy_ip),
                ("network.proxy.ssl_port", proxy_port),
                ("network.proxy.type", 1)
        ]

        _template_setting = "user_pref(\"{0}\", {1});\n"
        _template_setting_startswith = "user_pref(\"{0}\","

        t_path_prefs = self.work_folder + "/" + self.old_path + "/prefs.js"
        t_settings_result = []
        with open(t_path_prefs, 'r') as f_prefs:
            for line in f_prefs.readlines():
                for setting in t_settings_new:
                    if line.startswith(_template_setting_startswith.format(setting[0])):
                        break
                else:
                    t_settings_result.append(line)

        if proxy_ip.count(".") == 3:
            for setting in t_settings_new:
                t_settings_result.append(_template_setting.format(setting[0], setting[1]))

        with open(t_path_prefs, 'w') as f_prefs_new:
            f_prefs_new.writelines(t_settings_result)

    def disable_proxy(self):
        self.enable_proxy("", -1)


class FileProfileFirefox:

    def __init__(self):

        self.work_folder = getenv('APPDATA') + "/Mozilla/Firefox/"
        self.path_ini_file = self.work_folder + "profiles.ini"
        self.profiles_ini = configparser.ConfigParser()
        self.profiles_ini.read(self.path_ini_file)
        self._list_prof = []
        self._visible_list_prof = self._list_prof
        self._read_list_prof()
        self.text_filling = ""

    def enable_proxy(self, proxy_ip: str, proxy_port: int):
        for prof in self._list_prof:
            if prof.selected:
                prof.enable_proxy(proxy_ip, proxy_port)

    def disable_proxy(self):
        for prof in self._list_prof:
            if prof.selected:
                prof.disable_proxy()

    def _read_list_prof(self):
        index_prof = 0
        self._list_prof = []
        while ("Profile" + str(index_prof)) in self.profiles_ini.sections():
            self._list_prof.append(ProfileFirefoxConfigHandler(
                index_prof,
                self.profiles_ini.get("Profile" + str(index_prof), 'Name'),
                self.profiles_ini.get("Profile" + str(index_prof), 'Path'),
                self.work_folder
            ))
            index_prof += 1

    def import_profile(self, import_folder, signal_show):
        index_fpk = 0
        t_prof_new = []
        while isfile(import_folder + "/" + str(index_fpk) + ".fpk"):
            t_prof = ProfileFirefoxConfigHandler(work_folder=self.work_folder,
                                                 path_fpk=import_folder + "/" + str(index_fpk) + ".fpk")
            t_prof_new.append(t_prof)
            index_fpk += 1

        for prof in t_prof_new:
            if not prof.from_pack_check():
                raise Exception("Error import exist profile: " + prof.name)

        for index, prof in enumerate(t_prof_new):
            signal_show.emit("{0}/{1}".format(index, len(t_prof_new)))
            prof.from_pack()
            self._list_prof.append(prof)

    def export_profile(self, export_folder, signal_show):
        if not isdir(export_folder):
            mkdir(export_folder)

        t_prof_selection = self.only_selection()
        t_prof_count = len(t_prof_selection)
        for index, prof in enumerate(t_prof_selection):
            signal_show.emit("{0}/{1}".format(index, t_prof_count))
            prof.to_pack(export_folder + "/" + str(index))

    def save(self):
        t_path_ini_file_new = self.path_ini_file
        t_profiles_ini_new = configparser.ConfigParser()
        t_profiles_ini_new.optionxform = lambda option: option
        for num, prof in enumerate(list(self._list_prof)):
            prof.index = num
            t_section = "Profile" + str(num)
            t_profiles_ini_new.add_section(t_section)
            t_profiles_ini_new.set(t_section, "Name", prof.name)
            t_profiles_ini_new.set(t_section, "IsRelative", "1")
            t_profiles_ini_new.set(t_section, "Path", prof.path)

        with open(t_path_ini_file_new, 'w') as configfile:
            t_profiles_ini_new.write(configfile, space_around_delimiters=False)

    def filling(self, text: str):
        self.text_filling = text

    def _filling(self):
        self._visible_list_prof = []
        for prof in self._list_prof:
            if len(self.text_filling):
                if self.text_filling.lower() in prof.name.lower():
                    self._visible_list_prof.append(prof)
            else:
                self._visible_list_prof.append(prof)

    def only_selection(self):
        t_result = []
        for prof in self._list_prof:
            if prof.selected:
                t_result.append(prof)
        return t_result

    def clear_selection(self):
        for prof in self._list_prof:
            prof.selected = False

    def __str__(self):
        return "\n".join([str(x)for x in self._visible_list_prof])

    def __getitem__(self, item):
        self._filling()
        return self._visible_list_prof[item]

    def __setitem__(self, key, value):
        for num, prof in enumerate(list(self._list_prof)):
            if prof == self._visible_list_prof[key]:
                self._list_prof[num] = value
                self._visible_list_prof[key] = self._list_prof[num]

    def __delitem__(self, key):
        for num, prof in enumerate(list(self._list_prof)):
            if prof == self._visible_list_prof[key]:
                self._list_prof.pop(num)
        self._filling()

    def pop(self, index):
        del self[index]

    def __len__(self):
        self._filling()
        return len(self._visible_list_prof)
