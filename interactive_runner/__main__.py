import interactive_runner as lib

s = lib.Sources()
for l in s.languages.values():
    print("lname",l.name)
    print("lsname",l.styled_name)
    print("ldesc",l.description)
    print("lbc",l._build_command)
    print("ldni",l.check_dependencies_installed())
    print("lisc",l.is_compiled)
    print("lrcmd",l._run_command)
    print()
    for a in l.assignments.values():
        print("alang",a.language)
        print("aname",a.name)
        print("agivend",a.given_date)
        print("adesc",a.description)
        print("adirs",a.directions)
        try:
            a.run()
        except Exception as e:
            print("errrun",e)
        print()

