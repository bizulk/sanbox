# Introduction

I wanted to try VSCode to manage C/C++ project :

- generate build project files with IDE independent solution, multiplatform
- color edit, code browsing, etc...
- build & debug
- manage multiple project in a workspace

Also I wanted to test building with a WinAPI project.

You can do it directly with the C/C++ extension, but also add the cmake tool.
Microsoft and vscode community provide sufficient documentation for everything.


##  [Development tutorial with visual studio code](https://code.visualstudio.com/docs/cpp/config-msvc)

Note : 
- I  installed SDK & **le visual studio installer / "Développement desktop en C++** which seems more complete.

Link to the SDK kit  - not necessary since we installed with vs studio installer ! [kit de développement logiciel (SDK) Windows](https://developer.microsoft.com/fr-fr/windows/downloads/windows-sdk/)

Link to [Build tools for Visual Studio 2022](https://visualstudio.microsoft.com/fr/downloads/)

Below the capture for visual studion installer :
![capture](.\capture\visual_studio_installer.png)

Below the capture for the SDK : 
![capture](.\capture\sdk_installer.png)

**Conclusion :**

That Works, but the plugin is vscode dependent, I want to be independent from that. Otherwise I could stuck to codeblocks/vstudio.
Also I only see run/debug task, no control to build for clean/debug/release.
So let's try vscode / cmake.  
**IMPORTANT** We must call vscode from "Developper commande prompt" the get the right environnement, the tutorial provide some workaround about that.  

## [Get started with CMAKE](https://code.visualstudio.com/docs/cpp/cmake-linux)

There is also a [Detailed doc](https://github.com/microsoft/vscode-cmake-tools/tree/main/docs#cmake-tools-for-visual-studio-code-documentation)


**Conclusion :**

This what I was seeking for :) VSCode & C/C++ Extension & Cmakge tools extension.
Visual studion 

HOWEVER : how to manage workspace with cmake ? It does not seems possible to do so with this extension.

**Next step:**

Assess installeds tool "code quality" as the address Sanitizer for C/C++. Also the SDK install other tools.


## Autres ressources non évaluée 

[Tutoriel windows win32](https://learn.microsoft.com/en-us/windows/win32/learnwin32/prepare-your-development-environment)

Apprendre Cmake : check l'extension VScode : y'a des sources données.


    