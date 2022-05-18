class DjangoFormParser {
    constructor() {

    }

    get htmlString() {
        return this._htmlString;
    }

    parseHtmlString(name, htmlString) { 
        this._htmlString = htmlString;
        console.log(`${name} htmlString=${this.htmlString}`);
        // Examples:
        // <input type="text" name="login" placeholder="Username" autocomplete="username" maxlength="150" required id="id_login">
        // <input type="password" name="password" placeholder="Password" autocomplete="current-password" required id="id_password">
        // <input type="checkbox" name="remember" id="id_remember">
        //
        // 両端の < > を外せば、 string か、 string="string" のパターンになっているが、エスケープシーケンスが入っていると難しい
        // 決め打ちをしてしまうのが簡単
        const reLogin = /<input type="text" name="login" placeholder="(.*)" autocomplete="(.*)" maxlength="(\d+)" required id="(\w+)">/;
        const rePassword = /<input type="password" name="password" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;
        const reRemember = /<input type="checkbox" name="remember" id="(\w+)">/;

        let groupsLogin = reLogin.exec(htmlString);
        if (groupsLogin) {
            console.log(`groupsLogin placeholder=[${groupsLogin[1]}] autocomplete=[${groupsLogin[2]}] maxlength=[${groupsLogin[3]}] id=[${groupsLogin[4]}]`)

            return {
                type: "text",
                name: "login",
                placeholder: groupsLogin[1],
                autocomplete: groupsLogin[2],
                maxlength: parseInt(groupsLogin[3]),
                id: groupsLogin[4],
            };
        }

        let groupsPassword = rePassword.exec(htmlString);
        if (groupsPassword) {
            console.log(`groupsPassword placeholder=[${groupsPassword[1]}] autocomplete=[${groupsPassword[2]}] id=[${groupsPassword[3]}]`)

            return {
                type: "password",
                name: "password",
                placeholder: groupsPassword[1],
                autocomplete: groupsPassword[2],
                id: groupsPassword[3],
            }
        }

        let groupsRemember = reRemember.exec(htmlString);
        if (groupsRemember) {
            console.log(`groupsRemember id=[${groupsRemember[1]}]`)

            return {
                type: "checkbox",
                name: "remember",
                id: groupsRemember[1],
            }
        }

        return {
            type: "undefined",
            name: "unknown",
        }
    }
}
