Aprofiler
=========

Unlike the others python profilers, this one is dedicated to profile your
application logic. You can emit(push/pop) events, or marks with information.
When you stop, the profiler will generate a json with all the events.
You can then generate HTML graphics out of it.

Let's say you got something like::

	def my_app_update():
		if something_happened:
			foo += 1
		do_stuff()
		do_more_stuff()

You want to be able to see how much time is spent in both `do_stuff` and
`do_more_stuff`, and maybe within then. So you can change your application code
to include a profiler::

	from aprofiler import profiler
	profiler.start()

	def my_app_update():
		profiler.push('mainloop')

		if something_happen:
			foo += 1
			profiler.mark('something happened, foo is now', foo)

		profiler.push('do_stuff')
		do_stuff()
		profiler.pop('do_stuff')

		profiler.push('do_more_stuff')
		do_more_stuff()
		profiler.pop('do_more_stuff')

		profiler.pop('mainloop')

	# at the end
	profiler.stop()

When the profiler stop, it will generate a .json with all the events generated.

Now you can create your own converter to generate cool graphics. Have a look at
example to see how we used in the Kivy project:

[![Frame profiling](https://github.com/kivy/aprofiler/raw/master/examples/generate-frame-graph.png)](#framegraph)

