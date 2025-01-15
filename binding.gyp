{
	'target_defaults': {
		'default_configuration': 'Release',
		'configurations': {
			'Release': {
				'cflags': [ '-O3' ],
				'xcode_settings': {
					'GCC_OPTIMIZATION_LEVEL': '3',
					'GCC_GENERATE_DEBUGGING_SYMBOLS': 'NO',
				},
			}
		},
	},
	'targets': [
		{
			'target_name': 'fibers',
			'sources': [
				'src/fibers.cc',
				'src/coroutine.cc',
				'src/libcoro/coro.c',
				# Rebuild on header changes
				'src/coroutine.h',
				'src/libcoro/coro.h',
			],
			'cflags!': ['-ansi'],
			'defines': ['USE_CORO', 'CORO_GUARDPAGES=1'],
			'ldflags': ['-pthread'],
			'conditions': [
				['OS == "linux"',
					{
						'cflags_c': [ '-std=gnu11' ],
						'variables': {
							'USE_MUSL': '<!(ldd --version 2>&1 | head -n1 | grep "musl" | wc -l)',
						},
						'conditions': [
							['<(USE_MUSL) == 1',
								{'defines': ['CORO_ASM', '__MUSL__']},
								{'defines': ['CORO_UCONTEXT']}
							],
						],
					},
				],
				['OS == "mac"', {'defines': ['CORO_ASM']}],
				['target_arch == "arm64"',
					{
						# There's been problems getting real fibers working on arm
						'defines': ['CORO_UCONTEXT', '_XOPEN_SOURCE'],
						'defines!': ['CORO_PTHREAD', 'CORO_SJLJ', 'CORO_ASM'],
					},
				],
			],
		},
	],
}
