# Mandrix
#### A Python implementation for MailChimp's Mandrill API for the Unix shell!
Mandrill is a great API developed by MailChimp for managing emails. Their documentation is great and you can find it at [Mandrill API Docs](https://mandrillapp.com/api/docs/).
They have wrappers for Python, PHP and more, but they don't really have an easy way to use their API on the fly via the terminal. Since I don't like writing complicated stuff in Bash and I personally don't love C, I decided to write a wrapper in Python (Mandrill + Unix = Mandrix!) that would let you use their features as if it was a normal command! Keep reading the docs for more info!

## Installation
* Clone the repo in whatever directory you want: `git clone https://github.com/ferrerluis/room.git`
* While in the root directory of the repo, create a symbolic link from Mandrix to your binaries folder: ``ln -s `pwd`/mandrix ~/bin``
* If you have not before, add your binaries folder to your path: `$PATH=$PATH":~/bin"`. You may want to add that line of code to your .bashrc file so that it gets loaded when you log into your account.
* Make sure that you add a `key.txt` file in the same directory as `mandrix` that contains the Mandrill API key only. You can get this key from Mandrill's website by creating an account. It gives you 2000 emails for free and the service is pretty cheap even afterwards.

## Usage
The program can be run from any directory by typing `mandrix command options arguments`, where
* `command` is one of the available commands for Mandrix (only `send` for now),
* `options` are any of the options available for the specific command (e.g. `--message "Some text for the message"` in the case of the command `send`), and
* `arguments` are the mandatory arguments for such command.
You can check all the available options and mandatory arguments for a command by typing `mandrix command -h` (e.g. `mandrix send -h`).

## Contributing
I tried to make contributing super easy, so you can just create "modules" inside of the *commands* folder. They just have to meet one requisite: they must have a *run* function that accepts three parameters and returns the response text gotten from the server:
* A list of command-line parameters `options` (strings) that will be passed as the arguments for the ArgumentParser when parsing the arguments: `parser.parse_args(args=options)`.
* An ArgumentParser object `parser` that you will use for adding necessary arguments for the command and parsing them. The advantage of this is that it makes getting arguments and optional arguments from the command line pretty easy and effortless. It even builds a --help optional for you! You can check the *send.py* file as an example on how to use the ArgumentParser.
* The `key` to be used by the API. It will be a normal string.

If your file works, name it however you want the command to be named (e.g. add\_rejection.py) so the command is called like `mandrix add_rejection options arguments`.

For more information on the ArgumentParser object and how to use it, check out [Argparse](https://docs.python.org/3/library/argparse.html).

You can use the Mandrill wrapper for Python for building your modules, too. [Mandrill for Python](https://mandrillapp.com/api/docs/index.python.html).

#### Made with love by Luis Ferrer-Labarca
