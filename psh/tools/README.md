# Psh tools for writing harness tests

## The basic module description

The python module `basic` makes writing harness tests easier. It provides the Psh class with the following methods:

* `assert_expected(self, input, expected, msg)` - assert, that for a given input (for example some psh command) expected output is printed. The function also checks if there are no unwanted pieces of information and asserts the next psh prompt. It's possible to pass a regex in the `expected` argument. For now, it's required to add `EOL` for multi-line `expected` outputs. There is also a possibility to pass an additional message to print if the assertion fails.

* `assert_only_prompt(self)` - assert psh prompt with the appropriate esc sequence

* `assert_prompt(self, msg, timeout, catch_timeout)` - assert psh prompt by searching only for `'(psh)% '` in buffer (without checking an escape sequence). There is also a possibility to pass a message to print if the assertion fails and set timeout arguments.

* `assert_prompt_fail(self, msg, timeout)` - assert, that there is no psh prompt in the read buffer.

* `assert_exec(self, program, expected, msg)` - same as `assert_expected`, but input is selected appropriately for the current target platform (using sysexec or /bin/prog_name). So for example instead of using `assert_expected(input='/bin/psh')` or `assert_expected(input='sysexec psh')` use `assert_exec(program='psh')`.

* `exec_prog(self, prog)` - same as `assert_exec`, but without specified output assertion

* `send_cmd(self, cmd)` - same as `assert_expected`, but without specified output assertion

* `run(self)` - run psh

* `get_target(self)` - returns current target platform (for example `ia32-generic` or `armv7m7-imxrt106x`). This method is useful, when there are some differences between target platform environments.

## The usage examples

* The error statement assertion
  
  ```python
  from psh.tools.basic import Psh

  def harness(p):

      psh = Psh(p)
      psh.run()
      psh.assert_only_prompt()

      fname = 'nonexistentFile'
      cmd = f'cat {fname}'
      statement = f'cat: {fname} no such file'

      psh.assert_expected(input=cmd, expected=statement)
  ```


* The multi-line Hello World assertion (assuming that, `heeloworld` binary, which prints 'Hello\nWorld' is provided)

  ```python
  from psh.tools.basic import Psh, EOL

  def harness(p):

      psh = Psh(p)
      psh.run()
      psh.assert_only_prompt()

      result = 'Hello' + EOL + 'World'
      assert_exec(program=helloworld, expected=result)
  ```

* Using `exec_prog()` and `send_cmd()`

  ```python
  from psh.tools.basic import Psh

  def harness(p):

      psh = Psh(p)
      psh.run()
      psh.assert_only_prompt()

      exec_prog(prog='psh')
      send_cmd(cmd='kill 3')
  ```
