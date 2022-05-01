from libcst import *

Module(
    body=[
        FunctionDef(
            name=Name(value="to_path"),
            params=Parameters(
                params=[
                    Param(name=Name(value="parser")),
                    Param(name=Name(value="name")),
                ],
                kwonly_params=[
                    Param(
                        name=Name(value="replace_spaces"), default=Name(value="False")
                    ),
                ],
            ),
            body=IndentedBlock(
                body=[
                    If(
                        test=Call(
                            func=Name(value="isinstance"),
                            args=[
                                Arg(value=Name(value="name")),
                                Arg(value=Name(value="Path")),
                            ],
                        ),
                        body=IndentedBlock(
                            body=[
                                SimpleStatementLine(
                                    body=[Return(value=Name(value="name"))]
                                )
                            ]
                        ),
                    )
                ]
            ),
        )
    ]
)