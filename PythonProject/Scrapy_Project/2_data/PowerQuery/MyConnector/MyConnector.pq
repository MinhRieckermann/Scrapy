// This file contains your Data Connector logic
[Version = "1.0.0"]
section MyConnector;

[DataSource.Kind="MyConnector", Publish="MyConnector.Publish"]
shared MyConnector.Contents = (optional message as text) =>
    let
        _message = if (message <> null) then message else "(no message)",
        a = "Hello from MyConnector: " & _message
    in
        a;

// Data Source Kind description
MyConnector = [
    Authentication = [
        // Key = [],
        // UsernamePassword = [],
        // Windows = [],
        Anonymous = []
    ]
];

// Data Source UI publishing description
MyConnector.Publish = [
    Beta = true,
    Category = "Other",
    ButtonText = { Extension.LoadString("ButtonTitle"), Extension.LoadString("ButtonHelp") },
    LearnMoreUrl = "https://powerbi.microsoft.com/",
    SourceImage = MyConnector.Icons,
    SourceTypeImage = MyConnector.Icons
];

MyConnector.Icons = [
    Icon16 = { Extension.Contents("MyConnector16.png"), Extension.Contents("MyConnector20.png"), Extension.Contents("MyConnector24.png"), Extension.Contents("MyConnector32.png") },
    Icon32 = { Extension.Contents("MyConnector32.png"), Extension.Contents("MyConnector40.png"), Extension.Contents("MyConnector48.png"), Extension.Contents("MyConnector64.png") }
];
