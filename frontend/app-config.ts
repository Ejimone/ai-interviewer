import type { AppConfig } from './lib/types';

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'OpenCodehq',
  pageTitle: 'OpenCode AI Interviewer',
  pageDescription: 'Built By OpenCodehq',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#f54d0ba0',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#f54d0bff',
  startButtonText: 'Start call',
};
