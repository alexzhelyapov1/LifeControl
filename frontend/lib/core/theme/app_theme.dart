import 'package:flutter/material.dart';

const _seedColor = Colors.teal;

final appTheme = ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: _seedColor,
    brightness: Brightness.light,
  ),
  appBarTheme: const AppBarTheme(
    centerTitle: true,
  ),
);

final appThemeDark = ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: _seedColor,
    brightness: Brightness.dark,
  ),
  appBarTheme: const AppBarTheme(
    centerTitle: true,
  ),
);