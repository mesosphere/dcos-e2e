from pathlib import Path
from textwrap import dedent

datas = []

# version_file = dedent(
#     """\
#     def foo():
#         return 'ADAM'
#     # def get_versions():
#     #     return {"version": "0+HELLO", "full-revisionid": None,
#     #                 "dirty": None,
#     #                 "error": "unable to find root of source tree",
#     #             }
#     #
#     """
# )
#
# Path('src/foobar').write_text(version_file)

with open('MANIFEST.in') as manifest_file:
    for line in manifest_file.readlines():
        if line.startswith('recursive-include'):
            _, path, _ = line.split()
        else:
            _, path = line.split()
        if path.startswith('src/'):
            if Path(path).is_file():
                parent = Path(path).parent
                path = str(parent)

            path_without_src = path[len('src/'):]
            datas.append((path, path_without_src))


binaries = [Path('./bin/dcos-docker')]
cmd_in_container = []
for binary in binaries:
    cmd_in_container += [
        'pyinstaller',
        './bin/{binary}'.format(binary=binary.name),
        '--onefile',
    ]
    for data in datas:
        source, destination = data
        data_str = '{source}:{destination}'.format(
            source=source,
            destination=destination,
        )
        add_data_command = [
            '--add-data', data_str
        ]
        cmd_in_container += add_data_command

print(' '.join(cmd_in_container))
