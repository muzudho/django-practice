class DjangoAllauthFormParser {
    constructor() {

    }

    get htmlString() {
        return this._htmlString;
    }

    parseHtmlString(name, htmlString) { 
        this._htmlString = htmlString;
        console.log(`${name} htmlString=${this.htmlString}`);
        // Examples:
        //
        // signup.html
        // <input type="text" name="username" placeholder="Username" autocomplete="username" minlength="1" maxlength="150" required id="id_username">
        // <label for="id_email">E-mail (optional):</label></th><td><input type="email" name="email" placeholder="E-mail address" autocomplete="email" id="id_email">
        // <label for="id_password1">Password:</label></th><td><input type="password" name="password1" placeholder="Password" autocomplete="new-password" required id="id_password1">
        // <label for="id_password2">Password (again):</label></th><td><input type="password" name="password2" placeholder="Password (again)" autocomplete="new-password" required id="id_password2">
        //
        // login.html
        // <input type="text" name="login" placeholder="Username" autocomplete="username" maxlength="150" required id="id_login">
        // <input type="password" name="password" placeholder="Password" autocomplete="current-password" required id="id_password">
        // <input type="checkbox" name="remember" id="id_remember">
        //
        // 両端の < > を外せば、 string か、 string="string" のパターンになっているが、エスケープシーケンスが入っていると難しい
        // 決め打ちをしてしまうのが簡単

        // signup.html
        const reUsername = /<input type="text" name="username" placeholder="(.*)" autocomplete="(.*)" minlength="(\d+)" maxlength="(\d+)" required id="(\w+)">/;
        const reEmail = /<input type="email" name="email" placeholder="(.*)" autocomplete="(.*)" id="(\w+)">/;
        const rePassword1 = /<input type="password" name="password1" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;
        const rePassword2 = /<input type="password" name="password2" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;

        // login.html
        const reLogin = /<input type="text" name="login" placeholder="(.*)" autocomplete="(.*)" maxlength="(\d+)" required id="(\w+)">/;
        const rePassword = /<input type="password" name="password" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;
        const reRemember = /<input type="checkbox" name="remember" id="(\w+)">/;

        // signup.html username
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`username placeholder=[${groups[1]}] autocomplete=[${groups[2]}] minlength=[${groups[3]}] maxlength=[${groups[4]}] id=[${groups[5]}]`)

                return {
                    type: "text",
                    name: "username",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    minlength: parseInt(groups[3]),
                    maxlength: parseInt(groups[4]),
                    id: groups[5],
                };
            }
        }

        // signup.html email
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`email placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "email",
                    name: "email",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                };
            }
        }

        // signup.html password1
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`password1 placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "password",
                    name: "password1",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                };
            }
        }

        // signup.html password2
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`password2 placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "password",
                    name: "password2",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                };
            }
        }

        // login.html login
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`login placeholder=[${groups[1]}] autocomplete=[${groups[2]}] maxlength=[${groups[3]}] id=[${groups[4]}]`)

                return {
                    type: "text",
                    name: "login",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    maxlength: parseInt(groups[3]),
                    id: groups[4],
                };
            }
        }

        // login.html password
        {
            let groups = rePassword.exec(htmlString);
            if (groups) {
                console.log(`password placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "password",
                    name: "password",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                }
            }
        }

        // login.html remember
        {
            let groups = reRemember.exec(htmlString);
            if (groups) {
                console.log(`remember id=[${groups[1]}]`)

                return {
                    type: "checkbox",
                    name: "remember",
                    id: groups[1],
                }
            }
        }

        return {
            type: "undefined",
            name: "unknown",
        }
    }
}
