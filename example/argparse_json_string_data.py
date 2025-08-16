def AddExtra(json_str):
    extra_mock = ["#if defined(CONSTRUCTOR_GET_HELP_STRING)\n"]
    extra_mock.append("    //Parent object constructor will call getHelpString, so setup the expected call\n")
    extra_mock.append("    //before returning the pointer\n")
    extra_mock.append("    stringMockptr stringMock = reinterpret_cast<stringMockptr> (retPtr.get());   // NOLINT\n")
    extra_mock.append("    EXPECT_CALL(*stringMock, getHelpString()).WillOnce(Return(\"mock getHelpString\"));\n")
    extra_mock.append("    #endif //defined(CONSTRUCTOR_GET_HELP_STRING)\n")
    json_str.set_extra_mock(extra_mock)
