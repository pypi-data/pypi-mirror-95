CREATE TABLE fura.sitecfg (
   site_id INTEGER
  ,id varchar(256)
  ,descr varchar(256)
  ,value varchar(4096)
  ,modified_by varchar(64)
  ,tm_stamp TIMESTAMP
);
ALTER TABLE fura.sitecfg ADD PRIMARY KEY (
   site_id
  ,id
);
ALTER TABLE fura.tokensentry
   ALTER COLUMN site_id SET NOT NULL
  ,ALTER COLUMN token_cnt SET NOT NULL
  ,ALTER COLUMN last_poll SET NOT NULL
;
ALTER TABLE fura.tokensentry ADD CONSTRAINT tokensentry_fk_site FOREIGN KEY (site_id) REFERENCES fura.site;
INSERT INTO audit.cfg SELECT 'fura.config',        'id',                       'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.config');
INSERT INTO audit.cfg SELECT 'fura.func',          'id',                       'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.func');
INSERT INTO audit.cfg SELECT 'fura.site',          'id',                       'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.site');
INSERT INTO audit.cfg SELECT 'fura.sitecfg',       'site_id|id',               'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.sitecfg');
INSERT INTO audit.cfg SELECT 'fura.role',          'site_id|id',               'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.role');
INSERT INTO audit.cfg SELECT 'fura.rolefuncrel',   'site_id|role_id|func_id',  'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.rolefuncrel');
INSERT INTO audit.cfg SELECT 'fura.usr',           'site_id|id',               'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.usr');
INSERT INTO audit.cfg SELECT 'fura.usrtype',       'id',                       'modified_by|tm_stamp', NULL, NULL, NULL WHERE NOT EXISTS (SELECT id FROM audit.cfg WHERE id = 'fura.usrtype');
INSERT INTO fura.funcgrp VALUES('FURA-ADMIN', 'Fura Administration', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.funcgrp VALUES('FURA',       'Fura',                '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.cfg.create',    'FURA-ADMIN', 'Create a config',   'C', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.cfg.read',      'FURA-ADMIN', 'Read a config',     'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.cfg.update',    'FURA-ADMIN', 'Update a config',   'U', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.cfg.delete',    'FURA-ADMIN', 'Delete a config',   'D', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.site.create',   'FURA-ADMIN', 'Create a site',   'C', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.site.read',     'FURA-ADMIN', 'Read a site',     'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.site.update',   'FURA-ADMIN', 'Update a site',   'U', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.site.delete',   'FURA-ADMIN', 'Delete a site',   'D', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usrtype.create',   'FURA-ADMIN', 'Create a user type',   'C', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usrtype.read',     'FURA-ADMIN', 'Read a user type',     'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usrtype.update',   'FURA-ADMIN', 'Update a user type',   'U', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usrtype.delete',   'FURA-ADMIN', 'Delete a user type',   'D', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.site VALUES(1, 'FURA', 'Fura Administration', 'A', 'ZA', 'ZAR', '27', '[fura]', CURRENT_TIMESTAMP);
SELECT setval('fura.site_id_seq', 1);
INSERT INTO fura.config VALUES ('audit.denied.level',  'Audit Denied Level',              '100', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('audit.denied.age',    'Audit Denied Max Age (days)',     '90',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('audit.granted.level', 'Audit Granted Level',             '100', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('audit.granted.age',   'Audit Granted Max Age (days)',    '90',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('audit.usrlogin.age',  'Audit User Login Max Age (days)', '90',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('paths.salt',        'Salt directory', 'env/fura/salt',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('token.webkey',      'Web token key',  '{"k":"ADkGzwL3kKBljqhH-7OR7ZQeSLMx5rmihwuPVWfgjeM","kty":"oct"}', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('otp.sms.length',    'Length of SMS One Time Pins.', '6', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('otp.sms.content',   'Content of SMS OTP, [alpha, numeric, or alphanumeric]', 'numeric', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('otp.sms.timeout',   'Time-out for SMS OTPs in minutes',   '5',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('otp.email.length',  'Length of e-mail OTP.', '6', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('otp.email.content', 'Content of e-mail OTP, [alpha, numeric, or alphanumeric]', 'alphanumeric', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('otp.email.timeout', 'Time-out for auth reset emails in minutes', '10', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('loco.trigger.type', 'The Loco trigger interface to use.', 'local_db', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('loco.trigger.cfg',  'The Loco trigger config.', '{"dao" : "postgresql"}', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('authreset.urlmask.email', 'The URL mask to email the user.  Use $site, $usr, $tok, and $authtype for replacement.', 'http://fura_example.co.za/resetUserAuth?site=$site&usr=$usr&otp=$otp&authtype=$authtype&otpmethod=$otpmethod', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('authreset.urlmask.sms',   'The URL mask to sms the user.  Use $site, $usr, $otp, and $authtype for replacement.',   'http://fura_example.co.za/resetUserAuth?site=$site&usr=$usr&otp=$otp&authtype=$authtype&otpmethod=$otpmethod', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('authreset.support-email', 'The support email address to use for auth resets.', 'support@bitsmiths.co.za', '[FURA]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('loco.authreset',          'Reset account loco type to use.',        'fura.reset_passwd',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('loco.usrreg',             'New registration loco type to use.',     'fura.registration',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('loco.login_attempt',      'Failed login attempt loco type to use.', 'fura.login_attempt', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('loco.confirm_addr',       'Confirm address loco type to use.',      'fura.confirm_addr',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('auth-policy.P.descr', 'Auth password policy description.', 'Minimum ten characters, at least one uppercase letter, one lowercase letter, one number and one special character.', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.config VALUES ('auth-policy.P.regex', 'Auth passowrd policy regex.',       '^(?=.*?[A-Z])(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{10,}$', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.sitecfg VALUES (1, 'audit.denied.level',  'Audit Denied Level',              '100', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.sitecfg VALUES (1, 'audit.denied.age',    'Audit Denied Max Age (days)',     '90',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.sitecfg VALUES (1, 'audit.granted.level', 'Audit Granted Level',             '100', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.sitecfg VALUES (1, 'audit.granted.age',   'Audit Granted Max Age (days)',    '90',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.sitecfg VALUES (1, 'audit.usrlogin.age',  'Audit User Login Max Age (days)', '90',  '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.role VALUES (1, 'admin', 'Fura super user admin', 'S', 1, 60, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.usrtype VALUES ('sys',    'System User', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.usrtype VALUES ('client', 'Client User', '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.usr VALUES (
  1, 'admin', 'admin', 'A', 'Admin', 'Admin', NULL, CURRENT_DATE, NULL,
  'nicolas@bitsmiths.co.za', 'steven@bitsmiths.co.za', NULL, NULL, '[fura]', CURRENT_TIMESTAMP, 'sys',
  TRUE, TRUE, FALSE, FALSE, TRUE, TRUE, TRUE);
INSERT INTO fura.func VALUES('fura.role.create',   'FURA', 'Create a role',        'C', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.role.read',     'FURA', 'Read a role',          'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.role.update',   'FURA', 'Update a role',        'U', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.role.delete',   'FURA', 'Delete a role',        'D', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.rfr.add',       'FURA', 'Assign function to role',   'C', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.rfr.read',      'FURA', 'Read a role function',      'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.rfr.rem',       'FURA', 'Remove function from role', 'D', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.func.read',     'FURA', 'Read a function',        'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.funcgrp.read',  'FURA', 'Read a function group',  'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.service.create',  'FURA', 'Create a service matrix',    'C', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.service.read',    'FURA', 'Read a service matrix',      'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.service.update',  'FURA', 'Update a service matrix',    'U', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.service.delete',  'FURA', 'Delete a service matrix',    'D', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.create',      'FURA', 'Create a user',     'C', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.read',        'FURA', 'Read a user',       'R', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.update',      'FURA', 'Update a user',     'U', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.delete',      'FURA', 'Delete a user',     'D', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.activate',    'FURA', 'Activate a user',   'A', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.susp',        'FURA', 'Suspend a user',    'A', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.disable',     'FURA', 'Disable a user',    'A', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.reset-auth',  'FURA', 'Request a reset link (email) for a user.', 'O', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.reset-token', 'FURA', 'Request a token auth is reset (regenerated).', 'O', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.read-token',  'FURA', 'Read an auth token.', 'O', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO fura.func VALUES('fura.usr.setrole',     'FURA', 'Set a users role.', 'U', 'Y', 5, '[fura]', CURRENT_TIMESTAMP);
INSERT INTO loco.notype  SELECT 'fura.reset_passwd',       'A', 'Fura reset password',             'Fura', 10, NULL,       1,  5, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT id FROM loco.notype WHERE id = 'fura.reset_passwd');
INSERT INTO loco.notype  SELECT 'fura.registration',       'A', 'Fura new registration',           'Fura', 10, NULL,       1, 60, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT id FROM loco.notype WHERE id = 'fura.registration');
INSERT INTO loco.notype  SELECT 'fura.confirm_addr',       'A', 'Fura confirm email/sms address',  'Fura', 10, NULL,       1, 60, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT id FROM loco.notype WHERE id = 'fura.confirm_addr');
INSERT INTO loco.notype  SELECT 'fura.login_attempt',      'A', 'Fura failed login attempt',       'Fura', 10, '["sms"]',  1, 60, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT id FROM loco.notype WHERE id = 'fura.login_attempt');
INSERT INTO loco.notempl SELECT 'fura.reset_passwd',   'sms',   'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'sms'   AND notype_id = 'fura.reset_passwd');
INSERT INTO loco.notempl SELECT 'fura.reset_passwd',   'email', 'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'email' AND notype_id = 'fura.reset_passwd');
INSERT INTO loco.notempl SELECT 'fura.confirm_addr',   'sms',   'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'sms'   AND notype_id = 'fura.confirm_addr');
INSERT INTO loco.notempl SELECT 'fura.confirm_addr',   'email', 'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'email' AND notype_id = 'fura.confirm_addr');
INSERT INTO loco.notempl SELECT 'fura.login_attempt',  'sms',   'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'sms'   AND notype_id = 'fura.login_attempt');
INSERT INTO loco.notempl SELECT 'fura.login_attempt',  'email', 'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'email' AND notype_id = 'fura.login_attempt');
INSERT INTO loco.notempl SELECT 'fura.registration',   'sms',   'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'sms'   AND notype_id = 'fura.registration');
INSERT INTO loco.notempl SELECT 'fura.registration',   'email', 'A', NULL, '{}', NULL, '[fura]', CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT notype_id FROM loco.notempl WHERE corrtype_id = 'email' AND notype_id = 'fura.registration');
UPDATE loco.notempl SET templ = '{}', modified_by = '[orv]', tm_stamp = CURRENT_TIMESTAMP WHERE notype_id like 'fura.%';
UPDATE loco.notempl
SET templ = '{"msg": "You are about to reset your ${site_descr}, OTP: ${otp}"}'
WHERE corrtype_id = 'sms' AND notype_id = 'fura.reset_passwd';
UPDATE loco.notempl
SET templ = '{"subject": "${site_descr} Password Reset", "body-text": "${site_descr}\n\nReset Password OTP: ${otp}\n\nDidn`t request a new password? If you need any help don`t hesitate to contact us at: ${support_email}", "body-html": "<!DOCTYPE html><html><head><title>Password Reset</title><style type=''text/css''> body { font-size: 0.87em; color: #ffffff; text-align: center; height: 100%;} h1  {font-size: 2.1em;} a {color: inherit;} img { display:block; width:100%; margin:-8% 0;}.img-row { overflow:hidden; margin:0;}.wrapper-div { margin: auto; max-width:600px;background-color: #373535ff;}.body-text {padding-top: 7%;}.body-text, .new-password-div {font-size: 1.2em;}.new-password-div { margin: auto; background-color: #90c84bff; padding: 2%; max-width: 35%; margin-top: 5%; font-weight: bold; color: #000000;}.footer-div { padding-top: 0.2%; padding-bottom: 2%; max-height: 7.857em; margin-top: 10%; background-color: #373535ff;}.footer-div, .body-text { padding-left: 10%; padding-right: 10%;}</style></head><body><div class=''wrapper-div''><div class=''row''><div class=''body-text''><h1>${site_descr}</h1><p><h3>Reset Password OTP : </h3><h2>${otp}</h2></p><p>Or to reset to your account in one easy step click the button below.</p></div><a style=''text-decoration:none'' href=''${httplink}''><div class=''new-password-div''>Reset My Password</div></a></div><div class=''row''><div class=''footer-div''><p>Didn`t request a new password?  If you need any help don`t hesitate to <a href=''mailto:${support_email}?subject=Mail from Our Site''>contact us.</a></p></div></div></div></body></html>" }'
WHERE corrtype_id = 'email' AND notype_id = 'fura.reset_passwd';
UPDATE loco.notempl
SET templ = '{"msg": "Failed login attempt for ${site_descr} detected on ${datetime}, remaining attempts: ${remaining}"}'
WHERE corrtype_id = 'sms' AND notype_id = 'fura.login_attempt';
UPDATE loco.notempl
SET templ = '{"subject": "Failed Login Attemp", "body-text": "${site_descr}\n\nFailed login attempt detected on ${datetime}, remaining attempts: ${remaining}\n\nDidn`t try an login? If you need any help don`t hesitate to contact us at: ${support_email}", "body-html": "<!DOCTYPE html><html><head><title>Failed Login Attempt</title><style type=''text/css''> body { font-size: 0.87em; color: #ffffff; text-align: center; height: 100%;} h1  {font-size: 2.1em;} a {color: inherit;} img { display:block; width:100%; margin:-8% 0;}.img-row { overflow:hidden; margin:0;}.wrapper-div { margin: auto; max-width:600px;background-color: #373535ff;}.body-text {padding-top: 7%; font-size: 1.0em}.body-text, .body-text { padding-left: 10%; padding-right: 10%;}</style></head><body><div class=''wrapper-div''><div class=''row''><div class=''body-text''><h1>${site_descr}</h1><p><h3>Failed Login Attempt!</h3></p><p>Failed login attempt detected on ${datetime}, remaining attempts: ${remaining}</p><p>Didn`t attempt to login?  If you need any help don`t hesitate to <a href=''mailto:${support_email}?subject=Mail from Our Site''>contact us.</a></p><br></div></div></div></div></body></html>" }'
WHERE corrtype_id = 'email' AND notype_id = 'fura.login_attempt';
UPDATE loco.notempl
SET templ = '{"msg": "You are about to confirm your ${site_descr} cell number, OTP: ${otp}"}'
WHERE corrtype_id = 'sms' AND notype_id = 'fura.confirm_addr';
UPDATE loco.notempl
SET templ = '{"subject": "Confirm You E-mail Address", "body-text": "${site_descr}\n\nConfirm OTP: ${otp}\n", "body-html": "<!DOCTYPE html><html><head><title>Confirm E-mail Address</title><style type=''text/css''> body { font-size: 0.87em; color: #ffffff; text-align: center; height: 100%;} h1 {font-size: 2.1em;} a {color: inherit;} img { display:block; width:100%; margin:-8% 0;}.img-row { overflow:hidden; margin:0;}.wrapper-div { margin: auto; max-width:600px;background-color: #373535ff;}.body-text {padding-top: 7%;}.body-text, .body-text { padding-left: 10%; padding-right: 10%;}</style></head><body><div class=''wrapper-div''><div class=''img-row''><img src=''mail-hero.png''></div><div class=''row''><div class=''body-text''><h1>${site_descr}</h1><p><h3>Confirm Your E-mail Address OTP : </h3><h2>${otp}</h2></p><p>If you need any help don`t hesitate to <a href=''mailto:${support_email}?subject=Mail from Our Site''>contact us.</a></p><br></div></div></div></div></div></body></html>" }'
WHERE corrtype_id = 'email' AND notype_id = 'fura.confirm_addr';
UPDATE loco.notempl
SET templ = '{"msg": "Your are about to complete your account registration with ${site_descr}, OTP: ${otp}"}'
WHERE corrtype_id = 'sms' AND notype_id = 'fura.registration';
UPDATE loco.notempl
SET templ = '{"subject": "${site_descr} Account Registration", "body-text": "${site_descr}\n\nAccount Registration OTP: ${otp}\n\nDidn`t register with us. No problem you can safely ignore this email or don`t hesitate to contact us at: ${support_email}", "body-html": "<!DOCTYPE html><html><head><title>Account Registration</title><style type=''text/css''> body { font-size: 0.87em; color: #ffffff; text-align: center; height: 100%;} h1  {font-size: 2.1em;} a {color: inherit;} img { display:block; width:100%; margin:-8% 0;}.img-row { overflow:hidden; margin:0;}.wrapper-div { margin: auto; max-width:600px;background-color: #373535ff;}.body-text {padding-top: 7%;}.body-text, .new-password-div {font-size: 1.2em;}.new-password-div { margin: auto; background-color: #90c84bff; padding: 2%; max-width: 35%; margin-top: 5%; font-weight: bold; color: #000000;}.footer-div { padding-top: 0.2%; padding-bottom: 2%; max-height: 7.857em; margin-top: 10%; background-color: #373535ff;}.footer-div, .body-text { padding-left: 10%; padding-right: 10%;}</style></head><body><div class=''wrapper-div''><div class=''row''><div class=''body-text''><h1>${site_descr}</h1><p><h3>Account Registration OTP : </h3><h2>${otp}</h2></p><p>Or to register to your account in one easy step click the button below.</p></div><a style=''text-decoration:none'' href=''${httplink}''><div class=''new-password-div''>Register My Account</div></a></div><div class=''row''><div class=''footer-div''><p>Didn`t register an account with us?  No problem, you can ignore this email or don`t hesitate to <a href=''mailto:${support_email}?subject=Mail from Our Site''>contact us.</a></p></div></div></div></body></html>" }'
WHERE corrtype_id = 'email' AND notype_id = 'fura.registration';
