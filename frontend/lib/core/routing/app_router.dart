import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

// Placeholder screens
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/auth/presentation/login_screen.dart';

part 'app_router.g.dart';

// Private navigators
final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

@riverpod
GoRouter router(RouterRef ref) {
  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: const SplashRoute().location,
    routes: $appRoutes,
    // Логика редиректа будет добавлена на Этапе 3
  );
}

// ИСПОЛЬЗУЙТЕ ИМЕНОВАННЫЙ АРГУМЕНТ 'path'
@TypedGoRoute<SplashRoute>(path: '/splash')
class SplashRoute extends GoRouteData {
  const SplashRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const Scaffold(body: Center(child: CircularProgressIndicator()));
  }
}

// ИСПОЛЬЗУЙТЕ ИМЕНОВАННЫЙ АРГУМЕНТ 'path'
@TypedGoRoute<LoginRoute>(path: '/login')
class LoginRoute extends GoRouteData {
  const LoginRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const LoginScreen();
  }
}

// ИСПОЛЬЗУЙТЕ ИМЕНОВАННЫЙ АРГУМЕНТ 'path'
@TypedGoRoute<DashboardRoute>(path: '/dashboard')
class DashboardRoute extends GoRouteData {
  const DashboardRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const DashboardScreen();
  }
}