# Archived DOCX source text

Historical source only. Not an active specification. Paragraph IDs preserve original body order, not visible Word numbering. All authoritative status is in the five current specifications.

### D0

FreeCAD Plus UI & UX

### D1

This outline records the UI and workflow changes specified in our discussions and in this document. It also records fields and behavior that must be retained when those features change. It is a specification, not an implementation or release checklist. Workbench headings without specified changes remain reserved; this document does not catalog all Classic FreeCAD commands.

### D2

File Structure

### D3

Components

### D4

Use a component as the definition of both a part and an assembly. A component can own modeling history and contain linked instances of other components.

### D5

Separate the component definition from its instances. Creating one placed component must create exactly one linked instance, without displaying its definition as an additional assembly instance.

### D6

New Component creates a domestic or external definition without a placed instance. Add Component creates or selects a definition and places one linked instance under the active component.

### D7

Bodies, excluding independently imported dumb bodies

### D8

Keep the Body objects needed by the FreeCAD core as background implementation objects. Do not expose them as independently deletable rows in the component panes.

### D9

A modeling feature owns its background result. Deleting or changing the feature must maintain valid result ownership; a visible solid must not remain detached from its background Body.

### D10

Component panel

### D11

Replace the Model pane with Components and a separate Attributes pane.

### D12

Models is the first tab: domestic definitions first, then expandable imported-file groups containing all definitions and any nested imported files. Retain instance counts.

### D13

Keep a component definition in the file even when every linked instance has been removed. Removing an instance must not remove its definition or leave orphaned links.

### D14

Deleting a definition from Models, when supported, is a distinct operation from deleting an instance from Part Tree; it must not happen implicitly.

### D15

Part Tree replaces Component Structure and Assembly Structure. It lists linked component instances only.

### D16

Keep the file first as the pinned top-level container, with the FreeCAD icon and file name. Show component occurrences beneath it; Part001 is an ordinary component.

### D17

Allow Cut/Paste and drag/drop to rearrange the tree. Move existing instances without creating duplicate definitions or losing their links.

### D18

History replaces Model History and Part History. Show the sequential history of the active component.

### D19

Origin is always the first item, visible by default for the active component, and cannot be deleted.

### D20

Origin Planes is a separate child under Origin, hidden by default, and cannot be deleted.

### D21

Keep background Bodies out of both the component tree and History.

### D22

Names and numbering

### D23

Use untitled001 as the default file name.

### D24

Name the first automatically added part Part001, then use the next available Part002, Part003, and so on.

### D25

Number feature labels within each component. The first sketch is Sketch001 and the first background Body is Body001 in every component.

### D26

Use Origin rather than exposing globally suffixed labels such as Origin001. Preserve the internal identities required by FreeCAD separately from the displayed labels.

### D27

User Interfaces

### D28

Offer Plus UI and Classic UI through Edit > Preferences > General. Plus UI is the default. Show exactly one toolbar style at a time, including after startup, workbench changes and preference changes. Both styles retain the enhanced feature workflows; choosing Classic UI must not discard the fields specified below.

### D29

Toolbars

### D30

Classic Toolbars

### D31

All upstream workbenches, their toolbar groups and toolbar operations are outlined below. This Classic inventory is the exception to the surrounding documentâ€™s scoped Plus requirements. The source baseline is FreeCAD/FreeCAD revision b9609745048b, matching the recorded toolbar audit. Dropdown operations are nested beneath their button. Conditional and edit-only controls are included; availability depends on the build, preferences and installed dependencies. Shared toolbars are listed once. Menu-only commands and third-party addon workbenches are outside this toolbar inventory.Plus locations below reflect the October 3, 2026 owner build. Missing means no matching command or replacement is exposed in its Plus ribbon; some workbenches and optional integrations are absent from this build. N/A identifies an intentionally replaced control. Common toolbar and ribbon header controls apply to all modes. A > separator identifies a dropdown choice or task option.

### D32

Not Workbench Specific

### D33

File

### D34

New Document (New File)

### D35

All modes | Common toolbar | New File

### D36

Openâ€¦ (Open)

### D37

All modes | Common toolbar | Open

### D38

Save (Save)

### D39

All modes | Common toolbar | Save

### D40

Edit

### D41

Undo (Undo)

### D42

All modes | Common toolbar | Undo

### D43

Redo (Redo)

### D44

All modes | Common toolbar | Redo

### D45

Recompute (Recompute)

### D46

All modes | Common toolbar | Recompute

### D47

Clipboard

### D48

Cut (Cut)

### D49

All modes | Common toolbar | Cut

### D50

Copy (Copy)

### D51

All modes | Common toolbar | Copy

### D52

Paste (Paste)

### D53

All modes | Common toolbar | Paste

### D54

Workbench

### D55

Workbench Selector (Mode selector)

### D56

All modes | Ribbon header | Mode selector

### D57

Macro

### D58

Record Macro (Record Macro)

### D59

Assembly Mode | Home tab | Record Macro

### D60

CAM Mode | Home tab | Record Macro

### D61

Draft Mode | Home tab | Record Macro

### D62

Material Mode | Home tab | Record Macro

### D63

Part Mode | Home tab | Record Macro

### D64

Spreadsheet Mode | Home tab | Record Macro

### D65

Drawing Mode | Home tab | Record Macro

### D66

Test Framework Mode | Home tab | Record Macro

### D67

Macros (Macros)

### D68

Assembly Mode | Home tab | Macros

### D69

CAM Mode | Home tab | Macros

### D70

Draft Mode | Home tab | Macros

### D71

Material Mode | Home tab | Macros

### D72

Part Mode | Home tab | Macros

### D73

Spreadsheet Mode | Home tab | Macros

### D74

Drawing Mode | Home tab | Macros

### D75

Test Framework Mode | Home tab | Macros

### D76

Execute Macro (Execute Macro)

### D77

Assembly Mode | Home tab | Execute Macro

### D78

CAM Mode | Home tab | Execute Macro

### D79

Draft Mode | Home tab | Execute Macro

### D80

Material Mode | Home tab | Execute Macro

### D81

Part Mode | Home tab | Execute Macro

### D82

Spreadsheet Mode | Home tab | Execute Macro

### D83

Drawing Mode | Home tab | Execute Macro

### D84

Test Framework Mode | Home tab | Execute Macro

### D85

View

### D86

Fit All (Fit All)

### D87

Assembly Mode | View tab | Fit All

### D88

CAM Mode | View tab | Fit All

### D89

Draft Mode | View tab | Fit All

### D90

Material Mode | View tab | Fit All

### D91

Part Mode | View tab | Fit All

### D92

Design Mode | View tab | Fit All

### D93

Spreadsheet Mode | View tab | Fit All

### D94

Drawing Mode | View tab | Fit All

### D95

Test Framework Mode | View tab | Fit All

### D96

Fit Selection (Fit Selection)

### D97

Assembly Mode | View tab | Fit Selection

### D98

CAM Mode | View tab | Fit Selection

### D99

Draft Mode | View tab | Fit Selection

### D100

Material Mode | View tab | Fit Selection

### D101

Part Mode | View tab | Fit Selection

### D102

Design Mode | View tab | Fit Selection

### D103

Spreadsheet Mode | View tab | Fit Selection

### D104

Drawing Mode | View tab | Fit Selection

### D105

Test Framework Mode | View tab | Fit Selection

### D106

Standard Views (dropdown) (Standard Views)

### D107

Assembly Mode | View tab | Isometric

### D108

CAM Mode | View tab | Isometric

### D109

Draft Mode | View tab | Isometric

### D110

Material Mode | View tab | Isometric

### D111

Part Mode | View tab | Isometric

### D112

Design Mode | View tab | Standard Views

### D113

Spreadsheet Mode | View tab | Isometric

### D114

Drawing Mode | View tab | Isometric

### D115

Test Framework Mode | View tab | Isometric

### D116

Isometric (Isometric)

### D117

Assembly Mode | View tab | Isometric > Isometric

### D118

Assembly Mode | View tab | Isometric

### D119

CAM Mode | View tab | Isometric > Isometric

### D120

CAM Mode | View tab | Isometric

### D121

Draft Mode | View tab | Isometric > Isometric

### D122

Draft Mode | View tab | Isometric

### D123

Material Mode | View tab | Isometric > Isometric

### D124

Material Mode | View tab | Isometric

### D125

Part Mode | View tab | Isometric > Isometric

### D126

Part Mode | View tab | Isometric

### D127

Design Mode | View tab | Standard Views > Isometric

### D128

Design Mode | View tab | Isometric

### D129

Spreadsheet Mode | View tab | Isometric > Isometric

### D130

Spreadsheet Mode | View tab | Isometric

### D131

Drawing Mode | View tab | Isometric > Isometric

### D132

Drawing Mode | View tab | Isometric

### D133

Test Framework Mode | View tab | Isometric > Isometric

### D134

Test Framework Mode | View tab | Isometric

### D135

Front (Front)

### D136

Assembly Mode | View tab | Isometric > Front

### D137

Assembly Mode | View tab | Front

### D138

CAM Mode | View tab | Isometric > Front

### D139

CAM Mode | View tab | Front

### D140

Draft Mode | View tab | Isometric > Front

### D141

Draft Mode | View tab | Front

### D142

Material Mode | View tab | Isometric > Front

### D143

Material Mode | View tab | Front

### D144

Part Mode | View tab | Isometric > Front

### D145

Part Mode | View tab | Front

### D146

Design Mode | View tab | Standard Views > Front

### D147

Design Mode | View tab | Front

### D148

Spreadsheet Mode | View tab | Isometric > Front

### D149

Spreadsheet Mode | View tab | Front

### D150

Drawing Mode | View tab | Isometric > Front

### D151

Drawing Mode | View tab | Front

### D152

Test Framework Mode | View tab | Isometric > Front

### D153

Test Framework Mode | View tab | Front

### D154

Top (Top)

### D155

Assembly Mode | View tab | Isometric > Top

### D156

Assembly Mode | View tab | Top

### D157

CAM Mode | View tab | Isometric > Top

### D158

CAM Mode | View tab | Top

### D159

Draft Mode | View tab | Isometric > Top

### D160

Draft Mode | View tab | Top

### D161

Material Mode | View tab | Isometric > Top

### D162

Material Mode | View tab | Top

### D163

Part Mode | View tab | Isometric > Top

### D164

Part Mode | View tab | Top

### D165

Design Mode | View tab | Standard Views > Top

### D166

Design Mode | View tab | Top

### D167

Spreadsheet Mode | View tab | Isometric > Top

### D168

Spreadsheet Mode | View tab | Top

### D169

Drawing Mode | View tab | Isometric > Top

### D170

Drawing Mode | View tab | Top

### D171

Test Framework Mode | View tab | Isometric > Top

### D172

Test Framework Mode | View tab | Top

### D173

Right (Right)

### D174

Assembly Mode | View tab | Isometric > Right

### D175

Assembly Mode | View tab | Right

### D176

CAM Mode | View tab | Isometric > Right

### D177

CAM Mode | View tab | Right

### D178

Draft Mode | View tab | Isometric > Right

### D179

Draft Mode | View tab | Right

### D180

Material Mode | View tab | Isometric > Right

### D181

Material Mode | View tab | Right

### D182

Part Mode | View tab | Isometric > Right

### D183

Part Mode | View tab | Right

### D184

Design Mode | View tab | Standard Views > Right

### D185

Design Mode | View tab | Right

### D186

Spreadsheet Mode | View tab | Isometric > Right

### D187

Spreadsheet Mode | View tab | Right

### D188

Drawing Mode | View tab | Isometric > Right

### D189

Drawing Mode | View tab | Right

### D190

Test Framework Mode | View tab | Isometric > Right

### D191

Test Framework Mode | View tab | Right

### D192

Rear (Rear)

### D193

Assembly Mode | View tab | Isometric > Rear

### D194

Assembly Mode | View tab | Rear

### D195

CAM Mode | View tab | Isometric > Rear

### D196

CAM Mode | View tab | Rear

### D197

Draft Mode | View tab | Isometric > Rear

### D198

Draft Mode | View tab | Rear

### D199

Material Mode | View tab | Isometric > Rear

### D200

Material Mode | View tab | Rear

### D201

Part Mode | View tab | Isometric > Rear

### D202

Part Mode | View tab | Rear

### D203

Design Mode | View tab | Standard Views > Rear

### D204

Design Mode | View tab | Rear

### D205

Spreadsheet Mode | View tab | Isometric > Rear

### D206

Spreadsheet Mode | View tab | Rear

### D207

Drawing Mode | View tab | Isometric > Rear

### D208

Drawing Mode | View tab | Rear

### D209

Test Framework Mode | View tab | Isometric > Rear

### D210

Test Framework Mode | View tab | Rear

### D211

Bottom (Bottom)

### D212

Assembly Mode | View tab | Isometric > Bottom

### D213

Assembly Mode | View tab | Bottom

### D214

CAM Mode | View tab | Isometric > Bottom

### D215

CAM Mode | View tab | Bottom

### D216

Draft Mode | View tab | Isometric > Bottom

### D217

Draft Mode | View tab | Bottom

### D218

Material Mode | View tab | Isometric > Bottom

### D219

Material Mode | View tab | Bottom

### D220

Part Mode | View tab | Isometric > Bottom

### D221

Part Mode | View tab | Bottom

### D222

Design Mode | View tab | Standard Views > Bottom

### D223

Design Mode | View tab | Bottom

### D224

Spreadsheet Mode | View tab | Isometric > Bottom

### D225

Spreadsheet Mode | View tab | Bottom

### D226

Drawing Mode | View tab | Isometric > Bottom

### D227

Drawing Mode | View tab | Bottom

### D228

Test Framework Mode | View tab | Isometric > Bottom

### D229

Test Framework Mode | View tab | Bottom

### D230

Left (Left)

### D231

Assembly Mode | View tab | Isometric > Left

### D232

Assembly Mode | View tab | Left

### D233

CAM Mode | View tab | Isometric > Left

### D234

CAM Mode | View tab | Left

### D235

Draft Mode | View tab | Isometric > Left

### D236

Draft Mode | View tab | Left

### D237

Material Mode | View tab | Isometric > Left

### D238

Material Mode | View tab | Left

### D239

Part Mode | View tab | Isometric > Left

### D240

Part Mode | View tab | Left

### D241

Design Mode | View tab | Standard Views > Left

### D242

Design Mode | View tab | Left

### D243

Spreadsheet Mode | View tab | Isometric > Left

### D244

Spreadsheet Mode | View tab | Left

### D245

Drawing Mode | View tab | Isometric > Left

### D246

Drawing Mode | View tab | Left

### D247

Test Framework Mode | View tab | Isometric > Left

### D248

Test Framework Mode | View tab | Left

### D249

Align to Selection (Align to Selection)

### D250

Assembly Mode | View tab | Align to Selection

### D251

CAM Mode | View tab | Align to Selection

### D252

Draft Mode | View tab | Align to Selection

### D253

Material Mode | View tab | Align to Selection

### D254

Part Mode | View tab | Align to Selection

### D255

Design Mode | View tab | Align to Selection

### D256

Spreadsheet Mode | View tab | Align to Selection

### D257

Drawing Mode | View tab | Align to Selection

### D258

Test Framework Mode | View tab | Align to Selection

### D259

Draw Style (dropdown) (Draw Style)

### D260

Assembly Mode | View tab | As Is

### D261

CAM Mode | View tab | As Is

### D262

Draft Mode | View tab | As Is

### D263

Material Mode | View tab | As Is

### D264

Part Mode | View tab | As Is

### D265

Design Mode | View tab | Draw Style

### D266

Spreadsheet Mode | View tab | As Is

### D267

Drawing Mode | View tab | As Is

### D268

Test Framework Mode | View tab | As Is

### D269

As Is (As Is)

### D270

Assembly Mode | View tab | As Is > As Is

### D271

CAM Mode | View tab | As Is > As Is

### D272

Draft Mode | View tab | As Is > As Is

### D273

Material Mode | View tab | As Is > As Is

### D274

Part Mode | View tab | As Is > As Is

### D275

Design Mode | View tab | Draw Style > As Is

### D276

Spreadsheet Mode | View tab | As Is > As Is

### D277

Drawing Mode | View tab | As Is > As Is

### D278

Test Framework Mode | View tab | As Is > As Is

### D279

Points (Points)

### D280

Assembly Mode | View tab | As Is > Points

### D281

CAM Mode | View tab | As Is > Points

### D282

Draft Mode | View tab | As Is > Points

### D283

Material Mode | View tab | As Is > Points

### D284

Part Mode | View tab | As Is > Points

### D285

Design Mode | View tab | Draw Style > Points

### D286

Spreadsheet Mode | View tab | As Is > Points

### D287

Drawing Mode | View tab | As Is > Points

### D288

Test Framework Mode | View tab | As Is > Points

### D289

Wireframe (Wireframe)

### D290

Assembly Mode | View tab | As Is > Wireframe

### D291

CAM Mode | View tab | As Is > Wireframe

### D292

Draft Mode | View tab | As Is > Wireframe

### D293

Material Mode | View tab | As Is > Wireframe

### D294

Part Mode | View tab | As Is > Wireframe

### D295

Design Mode | View tab | Draw Style > Wireframe

### D296

Spreadsheet Mode | View tab | As Is > Wireframe

### D297

Drawing Mode | View tab | As Is > Wireframe

### D298

Test Framework Mode | View tab | As Is > Wireframe

### D299

Hidden Line (Hidden Line)

### D300

Assembly Mode | View tab | As Is > Hidden Line

### D301

CAM Mode | View tab | As Is > Hidden Line

### D302

Draft Mode | View tab | As Is > Hidden Line

### D303

Material Mode | View tab | As Is > Hidden Line

### D304

Part Mode | View tab | As Is > Hidden Line

### D305

Design Mode | View tab | Draw Style > Hidden Line

### D306

Spreadsheet Mode | View tab | As Is > Hidden Line

### D307

Drawing Mode | View tab | As Is > Hidden Line

### D308

Test Framework Mode | View tab | As Is > Hidden Line

### D309

No Shading (No Shading)

### D310

Assembly Mode | View tab | As Is > No Shading

### D311

CAM Mode | View tab | As Is > No Shading

### D312

Draft Mode | View tab | As Is > No Shading

### D313

Material Mode | View tab | As Is > No Shading

### D314

Part Mode | View tab | As Is > No Shading

### D315

Design Mode | View tab | Draw Style > No Shading

### D316

Spreadsheet Mode | View tab | As Is > No Shading

### D317

Drawing Mode | View tab | As Is > No Shading

### D318

Test Framework Mode | View tab | As Is > No Shading

### D319

Shaded (Shaded)

### D320

Assembly Mode | View tab | As Is > Shaded

### D321

CAM Mode | View tab | As Is > Shaded

### D322

Draft Mode | View tab | As Is > Shaded

### D323

Material Mode | View tab | As Is > Shaded

### D324

Part Mode | View tab | As Is > Shaded

### D325

Design Mode | View tab | Draw Style > Shaded

### D326

Spreadsheet Mode | View tab | As Is > Shaded

### D327

Drawing Mode | View tab | As Is > Shaded

### D328

Test Framework Mode | View tab | As Is > Shaded

### D329

Flat Lines (Flat Lines)

### D330

Assembly Mode | View tab | As Is > Flat Lines

### D331

CAM Mode | View tab | As Is > Flat Lines

### D332

Draft Mode | View tab | As Is > Flat Lines

### D333

Material Mode | View tab | As Is > Flat Lines

### D334

Part Mode | View tab | As Is > Flat Lines

### D335

Design Mode | View tab | Draw Style > Flat Lines

### D336

Spreadsheet Mode | View tab | As Is > Flat Lines

### D337

Drawing Mode | View tab | As Is > Flat Lines

### D338

Test Framework Mode | View tab | As Is > Flat Lines

### D339

Measure (Measure)

### D340

Assembly Mode | Home tab | Measure

### D341

Assembly Mode | View tab | Measure

### D342

CAM Mode | Home tab | Measure

### D343

CAM Mode | View tab | Measure

### D344

Draft Mode | Home tab | Measure

### D345

Draft Mode | View tab | Measure

### D346

Material Mode | Home tab | Measure

### D347

Material Mode | View tab | Measure

### D348

Part Mode | Home tab | Measure

### D349

Part Mode | View tab | Measure

### D350

Design Mode | View tab | Measure

### D351

Spreadsheet Mode | Home tab | Measure

### D352

Spreadsheet Mode | View tab | Measure

### D353

Drawing Mode | Home tab | Measure

### D354

Drawing Mode | View tab | Measure

### D355

Test Framework Mode | Home tab | Measure

### D356

Test Framework Mode | View tab | Measure

### D357

Mass Properties (Mass Properties)

### D358

Assembly Mode | Home tab | Mass Properties

### D359

Assembly Mode | View tab | Mass Properties

### D360

CAM Mode | Home tab | Mass Properties

### D361

CAM Mode | View tab | Mass Properties

### D362

Draft Mode | Home tab | Mass Properties

### D363

Draft Mode | View tab | Mass Properties

### D364

Material Mode | Home tab | Mass Properties

### D365

Material Mode | View tab | Mass Properties

### D366

Part Mode | Home tab | Mass Properties

### D367

Part Mode | View tab | Mass Properties

### D368

Design Mode | View tab | Mass Properties

### D369

Spreadsheet Mode | Home tab | Mass Properties

### D370

Spreadsheet Mode | View tab | Mass Properties

### D371

Drawing Mode | Home tab | Mass Properties

### D372

Drawing Mode | View tab | Mass Properties

### D373

Test Framework Mode | Home tab | Mass Properties

### D374

Test Framework Mode | View tab | Mass Properties

### D375

Individual Views

### D376

Isometric (Isometric)

### D377

Assembly Mode | View tab | Isometric > Isometric

### D378

Assembly Mode | View tab | Isometric

### D379

CAM Mode | View tab | Isometric > Isometric

### D380

CAM Mode | View tab | Isometric

### D381

Draft Mode | View tab | Isometric > Isometric

### D382

Draft Mode | View tab | Isometric

### D383

Material Mode | View tab | Isometric > Isometric

### D384

Material Mode | View tab | Isometric

### D385

Part Mode | View tab | Isometric > Isometric

### D386

Part Mode | View tab | Isometric

### D387

Design Mode | View tab | Standard Views > Isometric

### D388

Design Mode | View tab | Isometric

### D389

Spreadsheet Mode | View tab | Isometric > Isometric

### D390

Spreadsheet Mode | View tab | Isometric

### D391

Drawing Mode | View tab | Isometric > Isometric

### D392

Drawing Mode | View tab | Isometric

### D393

Test Framework Mode | View tab | Isometric > Isometric

### D394

Test Framework Mode | View tab | Isometric

### D395

Front (Front)

### D396

Assembly Mode | View tab | Isometric > Front

### D397

Assembly Mode | View tab | Front

### D398

CAM Mode | View tab | Isometric > Front

### D399

CAM Mode | View tab | Front

### D400

Draft Mode | View tab | Isometric > Front

### D401

Draft Mode | View tab | Front

### D402

Material Mode | View tab | Isometric > Front

### D403

Material Mode | View tab | Front

### D404

Part Mode | View tab | Isometric > Front

### D405

Part Mode | View tab | Front

### D406

Design Mode | View tab | Standard Views > Front

### D407

Design Mode | View tab | Front

### D408

Spreadsheet Mode | View tab | Isometric > Front

### D409

Spreadsheet Mode | View tab | Front

### D410

Drawing Mode | View tab | Isometric > Front

### D411

Drawing Mode | View tab | Front

### D412

Test Framework Mode | View tab | Isometric > Front

### D413

Test Framework Mode | View tab | Front

### D414

Top (Top)

### D415

Assembly Mode | View tab | Isometric > Top

### D416

Assembly Mode | View tab | Top

### D417

CAM Mode | View tab | Isometric > Top

### D418

CAM Mode | View tab | Top

### D419

Draft Mode | View tab | Isometric > Top

### D420

Draft Mode | View tab | Top

### D421

Material Mode | View tab | Isometric > Top

### D422

Material Mode | View tab | Top

### D423

Part Mode | View tab | Isometric > Top

### D424

Part Mode | View tab | Top

### D425

Design Mode | View tab | Standard Views > Top

### D426

Design Mode | View tab | Top

### D427

Spreadsheet Mode | View tab | Isometric > Top

### D428

Spreadsheet Mode | View tab | Top

### D429

Drawing Mode | View tab | Isometric > Top

### D430

Drawing Mode | View tab | Top

### D431

Test Framework Mode | View tab | Isometric > Top

### D432

Test Framework Mode | View tab | Top

### D433

Right (Right)

### D434

Assembly Mode | View tab | Isometric > Right

### D435

Assembly Mode | View tab | Right

### D436

CAM Mode | View tab | Isometric > Right

### D437

CAM Mode | View tab | Right

### D438

Draft Mode | View tab | Isometric > Right

### D439

Draft Mode | View tab | Right

### D440

Material Mode | View tab | Isometric > Right

### D441

Material Mode | View tab | Right

### D442

Part Mode | View tab | Isometric > Right

### D443

Part Mode | View tab | Right

### D444

Design Mode | View tab | Standard Views > Right

### D445

Design Mode | View tab | Right

### D446

Spreadsheet Mode | View tab | Isometric > Right

### D447

Spreadsheet Mode | View tab | Right

### D448

Drawing Mode | View tab | Isometric > Right

### D449

Drawing Mode | View tab | Right

### D450

Test Framework Mode | View tab | Isometric > Right

### D451

Test Framework Mode | View tab | Right

### D452

Rear (Rear)

### D453

Assembly Mode | View tab | Isometric > Rear

### D454

Assembly Mode | View tab | Rear

### D455

CAM Mode | View tab | Isometric > Rear

### D456

CAM Mode | View tab | Rear

### D457

Draft Mode | View tab | Isometric > Rear

### D458

Draft Mode | View tab | Rear

### D459

Material Mode | View tab | Isometric > Rear

### D460

Material Mode | View tab | Rear

### D461

Part Mode | View tab | Isometric > Rear

### D462

Part Mode | View tab | Rear

### D463

Design Mode | View tab | Standard Views > Rear

### D464

Design Mode | View tab | Rear

### D465

Spreadsheet Mode | View tab | Isometric > Rear

### D466

Spreadsheet Mode | View tab | Rear

### D467

Drawing Mode | View tab | Isometric > Rear

### D468

Drawing Mode | View tab | Rear

### D469

Test Framework Mode | View tab | Isometric > Rear

### D470

Test Framework Mode | View tab | Rear

### D471

Bottom (Bottom)

### D472

Assembly Mode | View tab | Isometric > Bottom

### D473

Assembly Mode | View tab | Bottom

### D474

CAM Mode | View tab | Isometric > Bottom

### D475

CAM Mode | View tab | Bottom

### D476

Draft Mode | View tab | Isometric > Bottom

### D477

Draft Mode | View tab | Bottom

### D478

Material Mode | View tab | Isometric > Bottom

### D479

Material Mode | View tab | Bottom

### D480

Part Mode | View tab | Isometric > Bottom

### D481

Part Mode | View tab | Bottom

### D482

Design Mode | View tab | Standard Views > Bottom

### D483

Design Mode | View tab | Bottom

### D484

Spreadsheet Mode | View tab | Isometric > Bottom

### D485

Spreadsheet Mode | View tab | Bottom

### D486

Drawing Mode | View tab | Isometric > Bottom

### D487

Drawing Mode | View tab | Bottom

### D488

Test Framework Mode | View tab | Isometric > Bottom

### D489

Test Framework Mode | View tab | Bottom

### D490

Left (Left)

### D491

Assembly Mode | View tab | Isometric > Left

### D492

Assembly Mode | View tab | Left

### D493

CAM Mode | View tab | Isometric > Left

### D494

CAM Mode | View tab | Left

### D495

Draft Mode | View tab | Isometric > Left

### D496

Draft Mode | View tab | Left

### D497

Material Mode | View tab | Isometric > Left

### D498

Material Mode | View tab | Left

### D499

Part Mode | View tab | Isometric > Left

### D500

Part Mode | View tab | Left

### D501

Design Mode | View tab | Standard Views > Left

### D502

Design Mode | View tab | Left

### D503

Spreadsheet Mode | View tab | Isometric > Left

### D504

Spreadsheet Mode | View tab | Left

### D505

Drawing Mode | View tab | Isometric > Left

### D506

Drawing Mode | View tab | Left

### D507

Test Framework Mode | View tab | Isometric > Left

### D508

Test Framework Mode | View tab | Left

### D509

Structure

### D510

New Part (Add Component)

### D511

Assembly Mode | Home tab | Add Component

### D512

CAM Mode | Home tab | Add Component

### D513

Draft Mode | Home tab | Add Component

### D514

Material Mode | Home tab | Add Component

### D515

Part Mode | Home tab | Add Component

### D516

Design Mode | Home tab | Add Component

### D517

Spreadsheet Mode | Home tab | Add Component

### D518

Drawing Mode | Home tab | Add Component

### D519

Test Framework Mode | Home tab | Add Component

### D520

New Group (New Group)

### D521

Assembly Mode | Home tab | New Group

### D522

CAM Mode | Home tab | New Group

### D523

Draft Mode | Home tab | New Group

### D524

Material Mode | Home tab | New Group

### D525

Part Mode | Home tab | New Group

### D526

Spreadsheet Mode | Home tab | New Group

### D527

Drawing Mode | Home tab | New Group

### D528

Test Framework Mode | Home tab | New Group

### D529

Link Actions (dropdown) (Make Link)

### D530

Assembly Mode | Home tab | Make Link

### D531

CAM Mode | Home tab | Make Link

### D532

Draft Mode | Home tab | Make Link

### D533

Material Mode | Home tab | Make Link

### D534

Part Mode | Home tab | Make Link

### D535

Spreadsheet Mode | Home tab | Make Link

### D536

Drawing Mode | Home tab | Make Link

### D537

Test Framework Mode | Home tab | Make Link

### D538

Make Link (Make Link)

### D539

Assembly Mode | Home tab | Make Link > Make Link

### D540

CAM Mode | Home tab | Make Link > Make Link

### D541

Draft Mode | Home tab | Make Link > Make Link

### D542

Material Mode | Home tab | Make Link > Make Link

### D543

Part Mode | Home tab | Make Link > Make Link

### D544

Spreadsheet Mode | Home tab | Make Link > Make Link

### D545

Drawing Mode | Home tab | Make Link > Make Link

### D546

Test Framework Mode | Home tab | Make Link > Make Link

### D547

Make Sub-Link (Make Sub-Link)

### D548

Assembly Mode | Home tab | Make Link > Make Sub-Link

### D549

CAM Mode | Home tab | Make Link > Make Sub-Link

### D550

Draft Mode | Home tab | Make Link > Make Sub-Link

### D551

Material Mode | Home tab | Make Link > Make Sub-Link

### D552

Part Mode | Home tab | Make Link > Make Sub-Link

### D553

Spreadsheet Mode | Home tab | Make Link > Make Sub-Link

### D554

Drawing Mode | Home tab | Make Link > Make Sub-Link

### D555

Test Framework Mode | Home tab | Make Link > Make Sub-Link

### D556

Replace With Link (Replace With Link)

### D557

Assembly Mode | Home tab | Make Link > Replace With Link

### D558

CAM Mode | Home tab | Make Link > Replace With Link

### D559

Draft Mode | Home tab | Make Link > Replace With Link

### D560

Material Mode | Home tab | Make Link > Replace With Link

### D561

Part Mode | Home tab | Make Link > Replace With Link

### D562

Spreadsheet Mode | Home tab | Make Link > Replace With Link

### D563

Drawing Mode | Home tab | Make Link > Replace With Link

### D564

Test Framework Mode | Home tab | Make Link > Replace With Link

### D565

Unlink (Unlink)

### D566

Assembly Mode | Home tab | Make Link > Unlink

### D567

CAM Mode | Home tab | Make Link > Unlink

### D568

Draft Mode | Home tab | Make Link > Unlink

### D569

Material Mode | Home tab | Make Link > Unlink

### D570

Part Mode | Home tab | Make Link > Unlink

### D571

Spreadsheet Mode | Home tab | Make Link > Unlink

### D572

Drawing Mode | Home tab | Make Link > Unlink

### D573

Test Framework Mode | Home tab | Make Link > Unlink

### D574

Import Links (Import Links)

### D575

Assembly Mode | Home tab | Make Link > Import Links

### D576

CAM Mode | Home tab | Make Link > Import Links

### D577

Draft Mode | Home tab | Make Link > Import Links

### D578

Material Mode | Home tab | Make Link > Import Links

### D579

Part Mode | Home tab | Make Link > Import Links

### D580

Spreadsheet Mode | Home tab | Make Link > Import Links

### D581

Drawing Mode | Home tab | Make Link > Import Links

### D582

Test Framework Mode | Home tab | Make Link > Import Links

### D583

Import All Links (Import All Links)

### D584

Assembly Mode | Home tab | Make Link > Import All Links

### D585

CAM Mode | Home tab | Make Link > Import All Links

### D586

Draft Mode | Home tab | Make Link > Import All Links

### D587

Material Mode | Home tab | Make Link > Import All Links

### D588

Part Mode | Home tab | Make Link > Import All Links

### D589

Spreadsheet Mode | Home tab | Make Link > Import All Links

### D590

Drawing Mode | Home tab | Make Link > Import All Links

### D591

Test Framework Mode | Home tab | Make Link > Import All Links

### D592

Variable Set (Variable Set)

### D593

Assembly Mode | Home tab | Variable Set

### D594

CAM Mode | Home tab | Variable Set

### D595

Draft Mode | Home tab | Variable Set

### D596

Material Mode | Home tab | Variable Set

### D597

Part Mode | Home tab | Variable Set

### D598

Spreadsheet Mode | Home tab | Variable Set

### D599

Drawing Mode | Home tab | Variable Set

### D600

Test Framework Mode | Home tab | Variable Set

### D601

Help

### D602

What's This? (What's This?)

### D603

Assembly Mode | Home tab | What's This?

### D604

CAM Mode | Home tab | What's This?

### D605

Draft Mode | Home tab | What's This?

### D606

Material Mode | Home tab | What's This?

### D607

Part Mode | Home tab | What's This?

### D608

Spreadsheet Mode | Home tab | What's This?

### D609

Drawing Mode | Home tab | What's This?

### D610

Test Framework Mode | Home tab | What's This?

### D611

Sketcher

### D612

Geometry, constraint, tool and helper groups are used during sketch editing. Preferences can show grouped dropdowns or individual buttons; both native forms are included.

### D613

Sketcher

### D614

New Sketch (New Sketch)

### D615

Part Mode | Tools tab | New Sketch

### D616

Design Mode | Sketch tab | New Sketch

### D617

Design Mode | Home tab | New Sketch

### D618

Design Mode | Modeling tab | New Sketch

### D619

Edit Sketch (Edit Sketch)

### D620

Design Mode | Modeling tab | Edit Sketch

### D621

Design Mode | Sketch tab | Edit Sketch

### D622

Attach Sketch (Attach Sketch)

### D623

Design Mode | Modeling tab | Attach Sketch

### D624

Design Mode | Sketch tab | Attach Sketch

### D625

Reorient Sketch (Reorient Sketch)

### D626

Design Mode | Sketch tab | Reorient Sketch

### D627

Validate Sketch (Validate Sketch)

### D628

Design Mode | Sketch tab | Validate Sketch

### D629

Merge Sketches (Merge Sketches)

### D630

Design Mode | Sketch tab | Merge Sketches

### D631

Mirror Sketch (Mirror Sketch)

### D632

Design Mode | Sketch tab | Mirror Sketch

### D633

Edit Mode

### D634

Leave Sketch (Leave Sketch)

### D635

Design Mode | Sketch tab | Leave Sketch

### D636

Align View to Sketch (Align View to Sketch)

### D637

Design Mode | Sketch tab | Align View to Sketch

### D638

Toggle Section View (Toggle Section View)

### D639

Design Mode | Sketch tab | Toggle Section View

### D640

Geometries

### D641

Point (Point)

### D642

Design Mode | Sketch tab | Point

### D643

Text (Experimental) (Text (Experimental))

### D644

Design Mode | Sketch tab | Text (Experimental)

### D645

Toggle Construction Geometry (Toggle Construction Geometry)

### D646

Design Mode | Sketch tab | Toggle Construction Geometry

### D647

Line Tools (dropdown) (Line Tools)

### D648

Design Mode | Sketch tab | Line Tools

### D649

Polyline (Polyline)

### D650

Design Mode | Sketch tab | Line Tools > Polyline

### D651

Design Mode | Sketch tab | Polyline

### D652

Line (Line)

### D653

Design Mode | Sketch tab | Line Tools > Line

### D654

Design Mode | Sketch tab | Line

### D655

Polyline (individual button option) (Polyline)

### D656

Design Mode | Sketch tab | Line Tools > Polyline

### D657

Design Mode | Sketch tab | Polyline

### D658

Line (individual button option) (Line)

### D659

Design Mode | Sketch tab | Line Tools > Line

### D660

Design Mode | Sketch tab | Line

### D661

Arc Tools (dropdown) (Arc Tools)

### D662

Design Mode | Sketch tab | Arc Tools

### D663

Arc From Center (Arc From Center)

### D664

Design Mode | Sketch tab | Arc Tools > Arc From Center

### D665

Arc From 3 Points (Arc From 3 Points)

### D666

Design Mode | Sketch tab | Arc Tools > Arc From 3 Points

### D667

Elliptical Arc (Elliptical Arc)

### D668

Design Mode | Sketch tab | Arc Tools > Elliptical Arc

### D669

Hyperbolic Arc (Hyperbolic Arc)

### D670

Design Mode | Sketch tab | Arc Tools > Hyperbolic Arc

### D671

Parabolic Arc (Parabolic Arc)

### D672

Design Mode | Sketch tab | Arc Tools > Parabolic Arc

### D673

Circle and Conic Tools (dropdown) (Circle and Conic Tools)

### D674

Design Mode | Sketch tab | Circle and Conic Tools

### D675

Circle From Center (Circle From Center)

### D676

Design Mode | Sketch tab | Circle and Conic Tools > Circle From Center

### D677

Circle From 3 Points (Circle From 3 Points)

### D678

Design Mode | Sketch tab | Circle and Conic Tools > Circle From 3 Points

### D679

Ellipse From Center (Ellipse From Center)

### D680

Design Mode | Sketch tab | Circle and Conic Tools > Ellipse From Center

### D681

Ellipse From 3 Points (Ellipse From 3 Points)

### D682

Design Mode | Sketch tab | Circle and Conic Tools > Ellipse From 3 Points

### D683

Rectangle Tools (dropdown) (Rectangle Tools)

### D684

Design Mode | Sketch tab | Rectangle Tools

### D685

Rectangle (Rectangle)

### D686

Design Mode | Sketch tab | Rectangle Tools > Rectangle

### D687

Centered Rectangle (Centered Rectangle)

### D688

Design Mode | Sketch tab | Rectangle Tools > Centered Rectangle

### D689

Rounded Rectangle (Rounded Rectangle)

### D690

Design Mode | Sketch tab | Rectangle Tools > Rounded Rectangle

### D691

Regular Polygon Tools (dropdown) (Regular Polygon Tools)

### D692

Design Mode | Sketch tab | Regular Polygon Tools

### D693

Triangle (Triangle)

### D694

Design Mode | Sketch tab | Regular Polygon Tools > Triangle

### D695

Square (Square)

### D696

Design Mode | Sketch tab | Regular Polygon Tools > Square

### D697

Pentagon (Pentagon)

### D698

Design Mode | Sketch tab | Regular Polygon Tools > Pentagon

### D699

Hexagon (Hexagon)

### D700

Design Mode | Sketch tab | Regular Polygon Tools > Hexagon

### D701

Heptagon (Heptagon)

### D702

Design Mode | Sketch tab | Regular Polygon Tools > Heptagon

### D703

Octagon (Octagon)

### D704

Design Mode | Sketch tab | Regular Polygon Tools > Octagon

### D705

Polygon (Polygon)

### D706

Design Mode | Sketch tab | Regular Polygon Tools > Polygon

### D707

Slot Tools (dropdown) (Slot Tools)

### D708

Design Mode | Sketch tab | Slot Tools

### D709

Slot (Slot)

### D710

Design Mode | Sketch tab | Slot Tools > Slot

### D711

Arc Slot (Arc Slot)

### D712

Design Mode | Sketch tab | Slot Tools > Arc Slot

### D713

B-Spline Creation Tools (dropdown) (B-Spline Creation Tools)

### D714

Design Mode | Sketch tab | B-Spline Creation Tools

### D715

B-Spline (B-Spline)

### D716

Design Mode | Sketch tab | B-Spline Creation Tools > B-Spline

### D717

Periodic B-Spline (Periodic B-Spline)

### D718

Design Mode | Sketch tab | B-Spline Creation Tools > Periodic B-Spline

### D719

B-Spline From Knots (B-Spline From Knots)

### D720

Design Mode | Sketch tab | B-Spline Creation Tools > B-Spline From Knots

### D721

Periodic B-Spline From Knots (Periodic B-Spline From Knots)

### D722

Design Mode | Sketch tab | B-Spline Creation Tools > Periodic B-Spline From Knots

### D723

Constraints

### D724

Dimension Tools (dropdown) (Dimension Tools)

### D725

Design Mode | Sketch tab | Dimension Tools

### D726

Dimension (Dimension)

### D727

Design Mode | Sketch tab | Dimension Tools > Dimension

### D728

Design Mode | Sketch tab | Dimension

### D729

Horizontal Dimension (Horizontal Dimension)

### D730

Design Mode | Sketch tab | Dimension Tools > Horizontal Dimension

### D731

Design Mode | Sketch tab | Horizontal Dimension

### D732

Vertical Dimension (Vertical Dimension)

### D733

Design Mode | Sketch tab | Dimension Tools > Vertical Dimension

### D734

Design Mode | Sketch tab | Vertical Dimension

### D735

Distance Dimension (Distance Dimension)

### D736

Design Mode | Sketch tab | Dimension Tools > Distance Dimension

### D737

Design Mode | Sketch tab | Distance Dimension

### D738

Radius/Diameter Dimension (Radius/Diameter Dimension)

### D739

Design Mode | Sketch tab | Dimension Tools > Radius/Diameter Dimension

### D740

Design Mode | Sketch tab | Radius and Diameter Constraints > Constrain auto radius/diameter

### D741

Radius Dimension (Radius Dimension)

### D742

Design Mode | Sketch tab | Dimension Tools > Radius Dimension

### D743

Design Mode | Sketch tab | Radius and Diameter Constraints > Constrain radius

### D744

Diameter Dimension (Diameter Dimension)

### D745

Design Mode | Sketch tab | Dimension Tools > Diameter Dimension

### D746

Design Mode | Sketch tab | Radius and Diameter Constraints > Constrain diameter

### D747

Angle Dimension (Angle Dimension)

### D748

Design Mode | Sketch tab | Dimension Tools > Angle Dimension

### D749

Design Mode | Sketch tab | Angle Dimension

### D750

Lock Position (Lock Position)

### D751

Design Mode | Sketch tab | Dimension Tools > Lock Position

### D752

Design Mode | Sketch tab | Lock Position

### D753

Dimension (individual button option) (Dimension)

### D754

Design Mode | Sketch tab | Dimension Tools > Dimension

### D755

Design Mode | Sketch tab | Dimension

### D756

Horizontal Dimension (individual button option) (Horizontal Dimension)

### D757

Design Mode | Sketch tab | Dimension Tools > Horizontal Dimension

### D758

Design Mode | Sketch tab | Horizontal Dimension

### D759

Vertical Dimension (individual button option) (Vertical Dimension)

### D760

Design Mode | Sketch tab | Dimension Tools > Vertical Dimension

### D761

Design Mode | Sketch tab | Vertical Dimension

### D762

Distance Dimension (individual button option) (Distance Dimension)

### D763

Design Mode | Sketch tab | Dimension Tools > Distance Dimension

### D764

Design Mode | Sketch tab | Distance Dimension

### D765

Radius and Diameter Constraints (dropdown) (Radius and Diameter Constraints)

### D766

Design Mode | Sketch tab | Radius and Diameter Constraints

### D767

Constrain radius (Constrain radius)

### D768

Design Mode | Sketch tab | Radius and Diameter Constraints > Constrain radius

### D769

Constrain diameter (Constrain diameter)

### D770

Design Mode | Sketch tab | Radius and Diameter Constraints > Constrain diameter

### D771

Constrain auto radius/diameter (Constrain auto radius/diameter)

### D772

Design Mode | Sketch tab | Radius and Diameter Constraints > Constrain auto radius/diameter

### D773

Angle Dimension (individual button option) (Angle Dimension)

### D774

Design Mode | Sketch tab | Dimension Tools > Angle Dimension

### D775

Design Mode | Sketch tab | Angle Dimension

### D776

Lock Position (individual button option) (Lock Position)

### D777

Design Mode | Sketch tab | Dimension Tools > Lock Position

### D778

Design Mode | Sketch tab | Lock Position

### D779

Coincident / Point-on-object (unified command) (Coincident / Point-on-object)

### D780

Design Mode | Sketch tab | Coincident / Point-on-object

### D781

Coincident Constraint (individual button option) (Coincident Constraint)

### D782

Design Mode | Sketch tab | Coincident Constraint

### D783

Point-on-object Constraint (individual button option) (Point-on-object Constraint)

### D784

Design Mode | Sketch tab | Point-on-object Constraint

### D785

Horizontal and Vertical Constraints (dropdown) (Horizontal and Vertical Constraints)

### D786

Design Mode | Sketch tab | Horizontal and Vertical Constraints

### D787

Horizontal Constraint (Horizontal Constraint)

### D788

Design Mode | Sketch tab | Horizontal and Vertical Constraints > Horizontal Constraint

### D789

Design Mode | Sketch tab | Horizontal Constraint

### D790

Vertical Constraint (Vertical Constraint)

### D791

Design Mode | Sketch tab | Horizontal and Vertical Constraints > Vertical Constraint

### D792

Design Mode | Sketch tab | Vertical Constraint

### D793

Horizontal Constraint (individual button option) (Horizontal Constraint)

### D794

Design Mode | Sketch tab | Horizontal and Vertical Constraints > Horizontal Constraint

### D795

Design Mode | Sketch tab | Horizontal Constraint

### D796

Vertical Constraint (individual button option) (Vertical Constraint)

### D797

Design Mode | Sketch tab | Horizontal and Vertical Constraints > Vertical Constraint

### D798

Design Mode | Sketch tab | Vertical Constraint

### D799

Parallel Constraint (Parallel Constraint)

### D800

Design Mode | Sketch tab | Parallel Constraint

### D801

Perpendicular Constraint (Perpendicular Constraint)

### D802

Design Mode | Sketch tab | Perpendicular Constraint

### D803

Tangent/Collinear Constraint (Tangent/Collinear Constraint)

### D804

Design Mode | Sketch tab | Tangent/Collinear Constraint

### D805

Equal Constraint (Equal Constraint)

### D806

Design Mode | Sketch tab | Equal Constraint

### D807

Symmetric Constraint (Symmetric Constraint)

### D808

Design Mode | Sketch tab | Symmetric Constraint

### D809

Block Constraint (Block Constraint)

### D810

Design Mode | Sketch tab | Block Constraint

### D811

Group Constraint (Development preview) (Group Constraint (Development preview))

### D812

Design Mode | Sketch tab | Group Constraint (Development preview)

### D813

Constraint State (dropdown) (Constraint State)

### D814

Design Mode | Sketch tab | Constraint State

### D815

Toggle Driving/Reference Constraints (Toggle Driving/Reference Constraints)

### D816

Design Mode | Sketch tab | Constraint State > Toggle Driving/Reference Constraints

### D817

Toggle Constraints (Toggle Constraints)

### D818

Design Mode | Sketch tab | Constraint State > Toggle Constraints

### D819

Sketcher Tools

### D820

External Geometry (dropdown) (External Geometry)

### D821

Design Mode | Sketch tab | External Geometry

### D822

External Projection (External Projection)

### D823

Design Mode | Sketch tab | External Geometry > External Projection

### D824

External Intersection (External Intersection)

### D825

Design Mode | Sketch tab | External Geometry > External Intersection

### D826

Carbon Copy (Carbon Copy)

### D827

Design Mode | Sketch tab | Carbon Copy

### D828

Move / Array Transform (Move / Array Transform)

### D829

Design Mode | Sketch tab | Move / Array Transform

### D830

Rotate / Polar Transform (Rotate / Polar Transform)

### D831

Design Mode | Sketch tab | Rotate / Polar Transform

### D832

Scale (Scale)

### D833

Design Mode | Sketch tab | Scale

### D834

Offset (Offset)

### D835

Design Mode | Sketch tab | Offset

### D836

Mirror (Mirror)

### D837

Design Mode | Sketch tab | Mirror

### D838

Remove Axes Alignment (Remove Axes Alignment)

### D839

Design Mode | Sketch tab | Remove Axes Alignment

### D840

Fillet and Chamfer Tools (dropdown) (Fillet and Chamfer Tools)

### D841

Design Mode | Sketch tab | Fillet and Chamfer Tools

### D842

Fillet (Fillet)

### D843

Design Mode | Sketch tab | Fillet and Chamfer Tools > Fillet

### D844

Chamfer (Chamfer)

### D845

Design Mode | Sketch tab | Fillet and Chamfer Tools > Chamfer

### D846

Curve Editing Tools (dropdown) (Curve Editing Tools)

### D847

Design Mode | Sketch tab | Curve Editing Tools

### D848

Trim Edge (Trim Edge)

### D849

Design Mode | Sketch tab | Curve Editing Tools > Trim Edge

### D850

Split Edge (Split Edge)

### D851

Design Mode | Sketch tab | Curve Editing Tools > Split Edge

### D852

Extend Edge (Extend Edge)

### D853

Design Mode | Sketch tab | Curve Editing Tools > Extend Edge

### D854

B-Spline Tools

### D855

Geometry to B-Spline (Geometry to B-Spline)

### D856

Design Mode | Sketch tab | Geometry to B-Spline

### D857

Increase B-Spline Degree (Increase B-Spline Degree)

### D858

Design Mode | Sketch tab | Increase B-Spline Degree

### D859

Decrease B-Spline Degree (Decrease B-Spline Degree)

### D860

Design Mode | Sketch tab | Decrease B-Spline Degree

### D861

Knot Multiplicity (dropdown) (Knot Multiplicity)

### D862

Design Mode | Sketch tab | Knot Multiplicity

### D863

Increase knot multiplicity (Increase knot multiplicity)

### D864

Design Mode | Sketch tab | Knot Multiplicity > Increase knot multiplicity

### D865

Decrease knot multiplicity (Decrease knot multiplicity)

### D866

Design Mode | Sketch tab | Knot Multiplicity > Decrease knot multiplicity

### D867

Insert Knot (Insert Knot)

### D868

Design Mode | Sketch tab | Insert Knot

### D869

Join Curves (Join Curves)

### D870

Design Mode | Sketch tab | Join Curves

### D871

Visual Helpers

### D872

Select Associated Constraints (Select Associated Constraints)

### D873

Design Mode | Sketch tab | Select Associated Constraints

### D874

Select Associated Geometry (Select Associated Geometry)

### D875

Design Mode | Sketch tab | Select Associated Geometry

### D876

Toggle Circular Helper for Arcs (Toggle Circular Helper for Arcs)

### D877

Design Mode | Sketch tab | Toggle Circular Helper for Arcs

### D878

B-Spline Geometry Information (dropdown) (B-Spline Geometry Information)

### D879

Design Mode | Sketch tab | B-Spline Geometry Information

### D880

Toggle B-Spline Degree (Toggle B-Spline Degree)

### D881

Design Mode | Sketch tab | B-Spline Geometry Information > Toggle B-Spline Degree

### D882

Toggle B-Spline Control Polygon (Toggle B-Spline Control Polygon)

### D883

Design Mode | Sketch tab | B-Spline Geometry Information > Toggle B-Spline Control Polygon

### D884

Toggle B-Spline Curvature Comb (Toggle B-Spline Curvature Comb)

### D885

Design Mode | Sketch tab | B-Spline Geometry Information > Toggle B-Spline Curvature Comb

### D886

Toggle B-Spline Knot Multiplicity (Toggle B-Spline Knot Multiplicity)

### D887

Design Mode | Sketch tab | B-Spline Geometry Information > Toggle B-Spline Knot Multiplicity

### D888

Toggle B-Spline Control Point Weight (Toggle B-Spline Control Point Weight)

### D889

Design Mode | Sketch tab | B-Spline Geometry Information > Toggle B-Spline Control Point Weight

### D890

Toggle Internal Geometry (Toggle Internal Geometry)

### D891

Design Mode | Sketch tab | Toggle Internal Geometry

### D892

Switch Virtual Space (Switch Virtual Space)

### D893

Design Mode | Sketch tab | Switch Virtual Space

### D894

Part Design

### D895

Part Design Helper Features

### D896

New Body (N/A, not needed)

### D897

Sketch Actions (dropdown) (N/A, separate sketch buttons replace this dropdown)

### D898

New Sketch (New Sketch)

### D899

Part Mode | Tools tab | New Sketch

### D900

Design Mode | Sketch tab | New Sketch

### D901

Design Mode | Home tab | New Sketch

### D902

Design Mode | Modeling tab | New Sketch

### D903

Attach Sketch (Attach Sketch)

### D904

Design Mode | Modeling tab | Attach Sketch

### D905

Design Mode | Sketch tab | Attach Sketch

### D906

Edit Sketch (Edit Sketch)

### D907

Design Mode | Modeling tab | Edit Sketch

### D908

Design Mode | Sketch tab | Edit Sketch

### D909

Validate Sketch (Validate Sketch)

### D910

Design Mode | Sketch tab | Validate Sketch

### D911

Check Geometry (Check Geometry)

### D912

Part Mode | Tools tab | Check Geometry

### D913

Sub-Shape Binder (missing)

### D914

Clone (missing)

### D915

Part Design Modeling Features

### D916

Pad (Extrude)

### D917

Design Mode | Home tab | Extrude

### D918

Design Mode | Modeling tab | Extrude

### D919

Revolve (Revolve)

### D920

Design Mode | Home tab | Revolve

### D921

Design Mode | Modeling tab | Revolve

### D922

Additive Loft (Loft)

### D923

Design Mode | Modeling tab | Loft

### D924

Additive Pipe (Pipe)

### D925

Native Pipe command retained; no button in the revised Modeling tab.

### D926

Additive Helix (Helix)

### D927

Design Mode | Modeling tab | Helix

### D928

Additive Primitives (dropdown) (Primitive)

### D929

Native Primitive command retained; use the large Primitives dropdown in Modeling.

### D930

Design Mode | Modeling tab | Primitives

### D931

Additive Box (Box)

### D932

Native primitive command | Box

### D933

Design Mode | Modeling tab | Primitives > Box

### D934

Additive Cylinder (Cylinder)

### D935

Native primitive command | Cylinder

### D936

Design Mode | Modeling tab | Primitives > Cylinder

### D937

Additive Sphere (Sphere)

### D938

Native primitive command | Sphere

### D939

Design Mode | Modeling tab | Primitives > Sphere

### D940

Additive Cone (Cone)

### D941

Native primitive command | Cone

### D942

Design Mode | Modeling tab | Primitives > Cone

### D943

Additive Ellipsoid (Ellipsoid)

### D944

Native primitive command | Ellipsoid

### D945

Design Mode | Modeling tab | Primitives > Ellipsoid

### D946

Additive Torus (Torus)

### D947

Native primitive command | Torus

### D948

Design Mode | Modeling tab | Primitives > Torus

### D949

Additive Prism (Prism)

### D950

Native primitive command | Prism

### D951

Design Mode | Modeling tab | Primitives > Prism

### D952

Additive Wedge (Wedge)

### D953

Native primitive command | Wedge

### D954

Design Mode | Modeling tab | Primitives > Wedge

### D955

Pocket (Extrude)

### D956

Design Mode | Home tab | Extrude

### D957

Design Mode | Modeling tab | Extrude

### D958

Hole (missing)

### D959

Groove (Revolve)

### D960

Design Mode | Home tab | Revolve

### D961

Design Mode | Modeling tab | Revolve

### D962

Subtractive Loft (Loft)

### D963

Design Mode | Modeling tab | Loft

### D964

Subtractive Pipe (Pipe)

### D965

Native Pipe command retained; no button in the revised Modeling tab.

### D966

Subtractive Helix (Helix)

### D967

Design Mode | Modeling tab | Helix

### D968

Subtractive Primitives (dropdown) (Primitive)

### D969

Native Primitive command retained; use the large Primitives dropdown in Modeling.

### D970

Design Mode | Modeling tab | Primitives

### D971

Subtractive Box (Box)

### D972

Native primitive command | Box

### D973

Design Mode | Modeling tab | Primitives > Box

### D974

Subtractive Cylinder (Cylinder)

### D975

Native primitive command | Cylinder

### D976

Design Mode | Modeling tab | Primitives > Cylinder

### D977

Subtractive Sphere (Sphere)

### D978

Native primitive command | Sphere

### D979

Design Mode | Modeling tab | Primitives > Sphere

### D980

Subtractive Cone (Cone)

### D981

Native primitive command | Cone

### D982

Design Mode | Modeling tab | Primitives > Cone

### D983

Subtractive Ellipsoid (Ellipsoid)

### D984

Native primitive command | Ellipsoid

### D985

Design Mode | Modeling tab | Primitives > Ellipsoid

### D986

Subtractive Torus (Torus)

### D987

Native primitive command | Torus

### D988

Design Mode | Modeling tab | Primitives > Torus

### D989

Subtractive Prism (Prism)

### D990

Native primitive command | Prism

### D991

Design Mode | Modeling tab | Primitives > Prism

### D992

Subtractive Wedge (Wedge)

### D993

Native primitive command | Wedge

### D994

Design Mode | Modeling tab | Primitives > Wedge

### D995

Boolean Operation (missing)

### D996

Part Design Dress-Up Features

### D997

Fillet (Fillet)

### D998

Design Mode | Home tab | Fillet/Chamfer

### D999

Design Mode | Home tab | Fillet/Chamfer > Fillet

### D1000

Design Mode | Modeling tab | Dress-Up | Fillet and Chamfer > Fillet (Default)

### D1001

Chamfer (Chamfer)

### D1002

Design Mode | Home tab | Fillet/Chamfer > Chamfer

### D1003

Design Mode | Modeling tab | Dress-Up | Fillet and Chamfer > Chamfer

### D1004

Draft (Draft)

### D1005

Design Mode | Modeling tab | Draft

### D1006

Thickness (Shell/Thickness)

### D1007

Design Mode | Modeling tab | Shell/Thickness

### D1008

Defeaturing (Delete Face/Defeaturing)

### D1009

Design Mode | Modeling tab | Other | Delete Face/Defeaturing

### D1010

Part Design Transformation Features

### D1011

Mirror (Mirror Feature)

### D1012

Design Mode | Modeling tab | Mirror Feature

### D1013

Linear Pattern (Linear Pattern)

### D1014

Design Mode | Modeling tab | Linear Pattern

### D1015

Polar Pattern (missing)

### D1016

Circular Pattern (Circular Pattern)

### D1017

Design Mode | Modeling tab | Circular Pattern

### D1018

Path Pattern (missing)

### D1019

Point Pattern (missing)

### D1020

Multi-Transform (Multi Transform)

### D1021

Design Mode | Modeling tab | Multi Transform

### D1022

Part

### D1023

Solids

### D1024

Cube (Cube)

### D1025

Part Mode | Home tab | Cube

### D1026

Part Mode | Tools tab | Cube

### D1027

Cylinder (Cylinder)

### D1028

Part Mode | Home tab | Cylinder

### D1029

Part Mode | Tools tab | Cylinder

### D1030

Sphere (Sphere)

### D1031

Part Mode | Home tab | Sphere

### D1032

Part Mode | Tools tab | Sphere

### D1033

Cone (Cone)

### D1034

Part Mode | Tools tab | Cone

### D1035

Torus (Torus)

### D1036

Part Mode | Tools tab | Torus

### D1037

Tube (Tube)

### D1038

Part Mode | Tools tab | Tube

### D1039

Primitive (Primitive)

### D1040

Part Mode | Tools tab | Primitive

### D1041

Shape Builder (Shape Builder)

### D1042

Part Mode | Tools tab | Shape Builder

### D1043

Part Tools

### D1044

New Sketch (New Sketch)

### D1045

Part Mode | Tools tab | New Sketch

### D1046

Design Mode | Sketch tab | New Sketch

### D1047

Design Mode | Home tab | New Sketch

### D1048

Design Mode | Modeling tab | New Sketch

### D1049

Extrude (Extrude)

### D1050

Part Mode | Tools tab | Extrude

### D1051

Revolve (Revolve)

### D1052

Part Mode | Tools tab | Revolve

### D1053

Mirror (Mirror)

### D1054

Part Mode | Tools tab | Mirror

### D1055

Scale (Scale)

### D1056

Part Mode | Tools tab | Scale

### D1057

Fillet (Fillet)

### D1058

Part Mode | Tools tab | Fillet

### D1059

Chamfer (Chamfer)

### D1060

Part Mode | Tools tab | Chamfer

### D1061

Face From Wires (Face From Wires)

### D1062

Part Mode | Tools tab | Face From Wires

### D1063

Ruled Surface (Ruled Surface)

### D1064

Part Mode | Tools tab | Ruled Surface

### D1065

Loft (Loft)

### D1066

Part Mode | Tools tab | Loft

### D1067

Sweep (Sweep)

### D1068

Part Mode | Tools tab | Sweep

### D1069

Section (Section)

### D1070

Part Mode | Tools tab | Section

### D1071

Cross-Sections (Cross-Sections)

### D1072

Part Mode | Tools tab | Cross-Sections

### D1073

Offset Tools (dropdown) (3D Offset)

### D1074

Part Mode | Tools tab | 3D Offset

### D1075

3D Offset (3D Offset)

### D1076

Part Mode | Tools tab | 3D Offset > 3D Offset

### D1077

2D Offset (2D Offset)

### D1078

Part Mode | Tools tab | 3D Offset > 2D Offset

### D1079

Thickness (Thickness)

### D1080

Part Mode | Tools tab | Thickness

### D1081

Project on Surface (Project on Surface)

### D1082

Part Mode | Tools tab | Project on Surface

### D1083

Appearance per Face (Appearance per Face)

### D1084

Part Mode | Tools tab | Appearance per Face

### D1085

Boolean Tools

### D1086

Compound Tools (dropdown) (Compound)

### D1087

Part Mode | Tools tab | Compound

### D1088

Compound (Compound)

### D1089

Part Mode | Tools tab | Compound > Compound

### D1090

Explode Compound (Explode Compound)

### D1091

Part Mode | Tools tab | Compound > Explode Compound

### D1092

Compound Filter (Compound Filter)

### D1093

Part Mode | Tools tab | Compound > Compound Filter

### D1094

Boolean Operation (Boolean Operation)

### D1095

Part Mode | Tools tab | Boolean Operation

### D1096

Cut (Cut)

### D1097

Part Mode | Tools tab | Cut

### D1098

Union (Union)

### D1099

Part Mode | Tools tab | Union

### D1100

Intersection (Intersection)

### D1101

Part Mode | Tools tab | Intersection

### D1102

Join Features (dropdown) (Connect Shapes)

### D1103

Part Mode | Tools tab | Connect Shapes

### D1104

Connect Shapes (Connect Shapes)

### D1105

Part Mode | Tools tab | Connect Shapes > Connect Shapes

### D1106

Embed Shapes (Embed Shapes)

### D1107

Part Mode | Tools tab | Connect Shapes > Embed Shapes

### D1108

Cutout Shape (Cutout Shape)

### D1109

Part Mode | Tools tab | Connect Shapes > Cutout Shape

### D1110

Split Features (dropdown) (Boolean Fragments)

### D1111

Part Mode | Tools tab | Boolean Fragments

### D1112

Boolean Fragments (Boolean Fragments)

### D1113

Part Mode | Tools tab | Boolean Fragments > Boolean Fragments

### D1114

Slice Apart (Slice Apart)

### D1115

Part Mode | Tools tab | Boolean Fragments > Slice Apart

### D1116

Slice to Compound (Slice to Compound)

### D1117

Part Mode | Tools tab | Boolean Fragments > Slice to Compound

### D1118

Boolean XOR (Boolean XOR)

### D1119

Part Mode | Tools tab | Boolean Fragments > Boolean XOR

### D1120

Check Geometry (Check Geometry)

### D1121

Part Mode | Tools tab | Check Geometry

### D1122

Defeaturing (Defeaturing)

### D1123

Part Mode | Tools tab | Defeaturing

### D1124

Surface

### D1125

Surface

### D1126

Filling (Filling)

### D1127

Design Mode | Surface tab | Filling

### D1128

Fill Boundary Curves (Fill Boundary Curves)

### D1129

Design Mode | Surface tab | Fill Boundary Curves

### D1130

Sections (Sections)

### D1131

Design Mode | Surface tab | Sections

### D1132

Extend Face (Extend Face)

### D1133

Design Mode | Surface tab | Extend Face

### D1134

Curve on Mesh (Curve on Mesh)

### D1135

Design Mode | Surface tab | Curve on Mesh

### D1136

Blend Curve (Blend Curve)

### D1137

Design Mode | Surface tab | Blend Curve

### D1138

Draft

### D1139

Draft Creation

### D1140

Line (Line)

### D1141

Draft Mode | Home tab | Line

### D1142

Draft Mode | Tools tab | Line

### D1143

Polyline (Polyline)

### D1144

Draft Mode | Home tab | Polyline

### D1145

Draft Mode | Tools tab | Polyline

### D1146

Fillet (Fillet)

### D1147

Draft Mode | Home tab | Fillet

### D1148

Draft Mode | Tools tab | Fillet

### D1149

Arc Tools (dropdown) (Arc)

### D1150

Draft Mode | Tools tab | Arc

### D1151

Arc (Arc)

### D1152

Draft Mode | Tools tab | Arc > Arc

### D1153

Arc From 3 Points (Arc From 3 Points)

### D1154

Draft Mode | Tools tab | Arc > Arc From 3 Points

### D1155

Circle (Circle)

### D1156

Draft Mode | Tools tab | Circle

### D1157

Ellipse (Ellipse)

### D1158

Draft Mode | Tools tab | Ellipse

### D1159

Rectangle (Rectangle)

### D1160

Draft Mode | Tools tab | Rectangle

### D1161

Polygon (Polygon)

### D1162

Draft Mode | Tools tab | Polygon

### D1163

B-Spline (B-Spline)

### D1164

Draft Mode | Tools tab | B-Spline

### D1165

BÃ©zier Tools (dropdown) (Cubic BÃ©zier Curve)

### D1166

Draft Mode | Tools tab | Cubic BÃ©zier Curve

### D1167

Cubic BÃ©zier Curve (Cubic BÃ©zier Curve)

### D1168

Draft Mode | Tools tab | Cubic BÃ©zier Curve > Cubic BÃ©zier Curve

### D1169

BÃ©zier Curve (BÃ©zier Curve)

### D1170

Draft Mode | Tools tab | Cubic BÃ©zier Curve > BÃ©zier Curve

### D1171

Point (Point)

### D1172

Draft Mode | Tools tab | Point

### D1173

Facebinder (Facebinder)

### D1174

Draft Mode | Tools tab | Facebinder

### D1175

Shape From Text (Shape From Text)

### D1176

Draft Mode | Tools tab | Shape From Text

### D1177

Hatch (Hatch)

### D1178

Draft Mode | Tools tab | Hatch

### D1179

Draft Annotation

### D1180

Text (Text)

### D1181

Draft Mode | Tools tab | Text

### D1182

Dimension (Dimension)

### D1183

Draft Mode | Tools tab | Dimension

### D1184

Label (Label)

### D1185

Draft Mode | Tools tab | Label

### D1186

Annotation Styles (Annotation Styles)

### D1187

Draft Mode | Tools tab | Annotation Styles

### D1188

Draft Modification

### D1189

Move (Move)

### D1190

Draft Mode | Tools tab | Move

### D1191

Rotate (Rotate)

### D1192

Draft Mode | Tools tab | Rotate

### D1193

Scale (Scale)

### D1194

Draft Mode | Tools tab | Scale

### D1195

Mirror (Mirror)

### D1196

Draft Mode | Tools tab | Mirror

### D1197

Offset (Offset)

### D1198

Draft Mode | Tools tab | Offset

### D1199

Trimex (Trimex)

### D1200

Draft Mode | Tools tab | Trimex

### D1201

Stretch (Stretch)

### D1202

Draft Mode | Tools tab | Stretch

### D1203

Clone (Clone)

### D1204

Draft Mode | Tools tab | Clone

### D1205

Array Tools (dropdown) (Array)

### D1206

Draft Mode | Tools tab | Array

### D1207

Array (Array)

### D1208

Draft Mode | Tools tab | Array > Array

### D1209

Polar Array (Polar Array)

### D1210

Draft Mode | Tools tab | Array > Polar Array

### D1211

Circular Array (Circular Array)

### D1212

Draft Mode | Tools tab | Array > Circular Array

### D1213

Path Array (Path Array)

### D1214

Draft Mode | Tools tab | Array > Path Array

### D1215

Path Link Array (Path Link Array)

### D1216

Draft Mode | Tools tab | Array > Path Link Array

### D1217

Point Array (Point Array)

### D1218

Draft Mode | Tools tab | Array > Point Array

### D1219

Point Link Array (Point Link Array)

### D1220

Draft Mode | Tools tab | Array > Point Link Array

### D1221

Twisted Path Array (Twisted Path Array)

### D1222

Draft Mode | Tools tab | Array > Twisted Path Array

### D1223

Twisted Path Link Array (Twisted Path Link Array)

### D1224

Draft Mode | Tools tab | Array > Twisted Path Link Array

### D1225

Edit (Edit)

### D1226

Draft Mode | Tools tab | Edit

### D1227

Highlight Subelements (Highlight Subelements)

### D1228

Draft Mode | Tools tab | Highlight Subelements

### D1229

Join (Join)

### D1230

Draft Mode | Tools tab | Join

### D1231

Split (Split)

### D1232

Draft Mode | Tools tab | Split

### D1233

Upgrade (Upgrade)

### D1234

Draft Mode | Tools tab | Upgrade

### D1235

Downgrade (Downgrade)

### D1236

Draft Mode | Tools tab | Downgrade

### D1237

Convert Wire/B-Spline (Convert Wire/B-Spline)

### D1238

Draft Mode | Tools tab | Convert Wire/B-Spline

### D1239

Draft to Sketch (Draft to Sketch)

### D1240

Draft Mode | Tools tab | Draft to Sketch

### D1241

Set Slope (Set Slope)

### D1242

Draft Mode | Tools tab | Set Slope

### D1243

Flip Dimension (Flip Dimension)

### D1244

Draft Mode | Tools tab | Flip Dimension

### D1245

2D View Tools (dropdown) (missing)

### D1246

Shape 2D View (Shape 2D View)

### D1247

Draft Mode | Tools tab | Shape 2D View

### D1248

Update Shape 2D View (missing)

### D1249

Draft Utility

### D1250

Manage Layers (Manage Layers)

### D1251

Draft Mode | Tools tab | Manage Layers

### D1252

New Named Group (New Named Group)

### D1253

Draft Mode | Tools tab | New Named Group

### D1254

Select Group (Select Group)

### D1255

Draft Mode | Tools tab | Select Group

### D1256

Add to Layer (Add to Layer)

### D1257

Draft Mode | Tools tab | Add to Layer

### D1258

Add to Group (Add to Group)

### D1259

Draft Mode | Tools tab | Add to Group

### D1260

Add to Construction Group (Add to Construction Group)

### D1261

Draft Mode | Tools tab | Add to Construction Group

### D1262

Toggle Wireframe (Toggle Wireframe)

### D1263

Draft Mode | Tools tab | Toggle Wireframe

### D1264

Working Plane Proxy (Working Plane Proxy)

### D1265

Draft Mode | Tools tab | Working Plane Proxy

### D1266

Draft Snap

### D1267

Snap Lock (Snap Lock)

### D1268

Draft Mode | Tools tab | Snap Lock

### D1269

Snap Endpoint (Snap Endpoint)

### D1270

Draft Mode | Tools tab | Snap Endpoint

### D1271

Snap Midpoint (Snap Midpoint)

### D1272

Draft Mode | Tools tab | Snap Midpoint

### D1273

Snap Center (Snap Center)

### D1274

Draft Mode | Tools tab | Snap Center

### D1275

Snap Angle (Snap Angle)

### D1276

Draft Mode | Tools tab | Snap Angle

### D1277

Snap Intersection (Snap Intersection)

### D1278

Draft Mode | Tools tab | Snap Intersection

### D1279

Snap Perpendicular (Snap Perpendicular)

### D1280

Draft Mode | Tools tab | Snap Perpendicular

### D1281

Snap Extension (Snap Extension)

### D1282

Draft Mode | Tools tab | Snap Extension

### D1283

Snap Parallel (Snap Parallel)

### D1284

Draft Mode | Tools tab | Snap Parallel

### D1285

Snap Special (Snap Special)

### D1286

Draft Mode | Tools tab | Snap Special

### D1287

Snap Near (Snap Near)

### D1288

Draft Mode | Tools tab | Snap Near

### D1289

Snap Ortho (Snap Ortho)

### D1290

Draft Mode | Tools tab | Snap Ortho

### D1291

Snap Grid (Snap Grid)

### D1292

Draft Mode | Tools tab | Snap Grid

### D1293

Snap Working Plane (Snap Working Plane)

### D1294

Draft Mode | Tools tab | Snap Working Plane

### D1295

Snap Dimensions (Snap Dimensions)

### D1296

Draft Mode | Tools tab | Snap Dimensions

### D1297

Toggle Grid (Toggle Grid)

### D1298

Draft Mode | Tools tab | Toggle Grid

### D1299

Assembly

### D1300

Assembly

### D1301

Create Assembly (Create Assembly)

### D1302

Assembly Mode | Home tab | New Assembly

### D1303

Assembly Mode | Tools tab | New Assembly

### D1304

Design Mode | Assembly tab | Create Assembly

### D1305

Insert Component (dropdown) (Insert Component)

### D1306

Assembly Mode | Home tab | Insert Component

### D1307

Assembly Mode | Tools tab | Insert Component

### D1308

Design Mode | Assembly tab | Insert Component

### D1309

Insert Component (Insert Component)

### D1310

Assembly Mode | Home tab | Insert Component > Insert Component

### D1311

Assembly Mode | Tools tab | Insert Component > Insert Component

### D1312

Design Mode | Assembly tab | Insert Component > Insert Component

### D1313

Insert New Part (Add Component)

### D1314

Assembly Mode | Home tab | Insert Component > Add Component

### D1315

Assembly Mode | Tools tab | Insert Component > Add Component

### D1316

Design Mode | Assembly tab | Insert Component > Insert New Part

### D1317

Link Arrays (dropdown) (Link Arrays)

### D1318

Assembly Mode | Home tab | Circular Link Array

### D1319

Assembly Mode | Tools tab | Circular Link Array

### D1320

Design Mode | Assembly tab | Link Arrays

### D1321

Circular Link Array (Circular Link Array)

### D1322

Assembly Mode | Home tab | Circular Link Array > Circular Link Array

### D1323

Assembly Mode | Tools tab | Circular Link Array > Circular Link Array

### D1324

Design Mode | Assembly tab | Link Arrays > Circular Link Array

### D1325

Linear Link Array (Linear Link Array)

### D1326

Assembly Mode | Home tab | Circular Link Array > Linear Link Array

### D1327

Assembly Mode | Tools tab | Circular Link Array > Linear Link Array

### D1328

Design Mode | Assembly tab | Link Arrays > Linear Link Array

### D1329

Path Link Array (Path Link Array)

### D1330

Assembly Mode | Home tab | Circular Link Array > Path Link Array

### D1331

Assembly Mode | Tools tab | Circular Link Array > Path Link Array

### D1332

Design Mode | Assembly tab | Link Arrays > Path Link Array

### D1333

Point Link Array (Point Link Array)

### D1334

Assembly Mode | Home tab | Circular Link Array > Point Link Array

### D1335

Assembly Mode | Tools tab | Circular Link Array > Point Link Array

### D1336

Design Mode | Assembly tab | Link Arrays > Point Link Array

### D1337

Polar Link Array (Polar Link Array)

### D1338

Assembly Mode | Home tab | Circular Link Array > Polar Link Array

### D1339

Assembly Mode | Tools tab | Circular Link Array > Polar Link Array

### D1340

Design Mode | Assembly tab | Link Arrays > Polar Link Array

### D1341

Solve Assembly (Solve Assembly)

### D1342

Assembly Mode | Tools tab | Solve Assembly

### D1343

Design Mode | Assembly tab | Solve Assembly

### D1344

Exploded View (Exploded View)

### D1345

Assembly Mode | Tools tab | Exploded View

### D1346

Design Mode | Assembly tab | Exploded View

### D1347

Snapshot (Snapshot)

### D1348

Assembly Mode | Tools tab | Snapshot

### D1349

Design Mode | Assembly tab | Snapshot

### D1350

Simulation (Simulation)

### D1351

Assembly Mode | Tools tab | Simulation

### D1352

Design Mode | Assembly tab | Simulation

### D1353

Bill of Materials (Bill of Materials)

### D1354

Assembly Mode | Tools tab | Bill of Materials

### D1355

Design Mode | Assembly tab | Bill of Materials

### D1356

Assembly Joints

### D1357

Toggle Grounded (Toggle Grounded)

### D1358

Assembly Mode | Tools tab | Toggle Grounded

### D1359

Design Mode | Assembly tab | Toggle Grounded

### D1360

Create Rigid Group (Create Rigid Group)

### D1361

Assembly Mode | Tools tab | Create Rigid Group

### D1362

Assembly Mode | Tools tab | Fixed Joint > Create Rigid Group

### D1363

Design Mode | Assembly tab | Create Rigid Group

### D1364

Fixed Joint (Fixed Joint)

### D1365

Assembly Mode | Tools tab | Fixed Joint

### D1366

Assembly Mode | Tools tab | Fixed Joint > Fixed Joint

### D1367

Design Mode | Assembly tab | Fixed Joint

### D1368

Revolute Joint (Revolute Joint)

### D1369

Assembly Mode | Tools tab | Fixed Joint > Revolute Joint

### D1370

Assembly Mode | Tools tab | Revolute Joint

### D1371

Design Mode | Assembly tab | Revolute Joint

### D1372

Cylindrical Joint (Cylindrical Joint)

### D1373

Assembly Mode | Tools tab | Fixed Joint > Cylindrical Joint

### D1374

Assembly Mode | Tools tab | Cylindrical Joint

### D1375

Design Mode | Assembly tab | Cylindrical Joint

### D1376

Slider Joint (Slider Joint)

### D1377

Assembly Mode | Tools tab | Fixed Joint > Slider Joint

### D1378

Assembly Mode | Tools tab | Slider Joint

### D1379

Design Mode | Assembly tab | Slider Joint

### D1380

Ball Joint (Ball Joint)

### D1381

Assembly Mode | Tools tab | Fixed Joint > Ball Joint

### D1382

Assembly Mode | Tools tab | Ball Joint

### D1383

Design Mode | Assembly tab | Ball Joint

### D1384

Distance Joint (Distance Joint)

### D1385

Assembly Mode | Tools tab | Fixed Joint > Distance Joint

### D1386

Assembly Mode | Tools tab | Distance Joint

### D1387

Design Mode | Assembly tab | Distance Joint

### D1388

Parallel Joint (Parallel Joint)

### D1389

Assembly Mode | Tools tab | Fixed Joint > Parallel Joint

### D1390

Assembly Mode | Tools tab | Parallel Joint

### D1391

Design Mode | Assembly tab | Parallel Joint

### D1392

Perpendicular Joint (Perpendicular Joint)

### D1393

Assembly Mode | Tools tab | Fixed Joint > Perpendicular Joint

### D1394

Assembly Mode | Tools tab | Perpendicular Joint

### D1395

Design Mode | Assembly tab | Perpendicular Joint

### D1396

Angle Joint (Angle Joint)

### D1397

Assembly Mode | Tools tab | Fixed Joint > Angle Joint

### D1398

Assembly Mode | Tools tab | Angle Joint

### D1399

Design Mode | Assembly tab | Angle Joint

### D1400

Rack and Pinion Joint (Rack and Pinion Joint)

### D1401

Assembly Mode | Tools tab | Fixed Joint > Rack and Pinion Joint

### D1402

Assembly Mode | Tools tab | Rack and Pinion Joint

### D1403

Design Mode | Assembly tab | Rack and Pinion Joint

### D1404

Screw Joint (Screw Joint)

### D1405

Assembly Mode | Tools tab | Fixed Joint > Screw Joint

### D1406

Assembly Mode | Tools tab | Screw Joint

### D1407

Design Mode | Assembly tab | Screw Joint

### D1408

Gears Joint (dropdown) (Gears Joint)

### D1409

Assembly Mode | Tools tab | Gears Joint

### D1410

Design Mode | Assembly tab | Gears Joint

### D1411

Gears Joint (Gears Joint)

### D1412

Assembly Mode | Tools tab | Fixed Joint > Gears Joint

### D1413

Assembly Mode | Tools tab | Gears Joint > Gears Joint

### D1414

Design Mode | Assembly tab | Gears Joint > Gears Joint

### D1415

Belt Joint (Belt Joint)

### D1416

Assembly Mode | Tools tab | Fixed Joint > Belt Joint

### D1417

Assembly Mode | Tools tab | Gears Joint > Belt Joint

### D1418

Design Mode | Assembly tab | Gears Joint > Belt Join

### D1419

Mesh

### D1420

Mesh Tools

### D1421

Import Meshâ€¦ (Import Mesh)

### D1422

Design Mode | Mesh tab | Import Mesh

### D1423

Export Meshâ€¦ (Export Mesh)

### D1424

Design Mode | Mesh tab | Export Mesh

### D1425

Mesh From Shape (Mesh From Shape)

### D1426

Design Mode | Mesh tab | Mesh From Shape

### D1427

Regular Solid (Regular Solid)

### D1428

Design Mode | Mesh tab | Regular Solid

### D1429

Mesh Modify

### D1430

Harmonize Normals (Harmonize Normals)

### D1431

Design Mode | Mesh tab | Harmonize Normals

### D1432

Flip Normals (Flip Normals)

### D1433

Design Mode | Mesh tab | Flip Normals

### D1434

Fill Holes (Fill Holes)

### D1435

Design Mode | Mesh tab | Fill Holes

### D1436

Close Hole (Close Hole)

### D1437

Design Mode | Mesh tab | Close Hole

### D1438

Add Triangle (Add Triangle)

### D1439

Design Mode | Mesh tab | Add Triangle

### D1440

Remove Components (Remove Components)

### D1441

Design Mode | Mesh tab | Remove Components

### D1442

Smooth (Smooth)

### D1443

Design Mode | Mesh tab | Smooth

### D1444

Refinement (Refinement)

### D1445

Design Mode | Mesh tab | Refinement

### D1446

Decimate (Decimate)

### D1447

Design Mode | Mesh tab | Decimate

### D1448

Scale (Scale)

### D1449

Design Mode | Mesh tab | Scale

### D1450

Mesh Boolean

### D1451

Union (Union)

### D1452

Design Mode | Mesh tab | Union

### D1453

Intersection (Intersection)

### D1454

Design Mode | Mesh tab | Intersection

### D1455

Difference (Difference)

### D1456

Design Mode | Mesh tab | Difference

### D1457

Mesh Cutting

### D1458

Cut (Cut)

### D1459

Design Mode | Mesh tab | Cut

### D1460

Trim (Trim)

### D1461

Design Mode | Mesh tab | Trim

### D1462

Trim With Plane (Trim With Plane)

### D1463

Design Mode | Mesh tab | Trim With Plane

### D1464

Section From Plane (Section From Plane)

### D1465

Design Mode | Mesh tab | Section From Plane

### D1466

Cross-Sections (Cross-Sections)

### D1467

Design Mode | Mesh tab | Cross-Sections

### D1468

Mesh Segmentation

### D1469

Merge (Merge)

### D1470

Design Mode | Mesh tab | Merge

### D1471

Split by Components (Split by Components)

### D1472

Design Mode | Mesh tab | Split by Components

### D1473

Segmentation (Segmentation)

### D1474

Design Mode | Mesh tab | Segmentation

### D1475

Segmentation From Best-Fit Surfaces (Segmentation From Best-Fit Surfaces)

### D1476

Design Mode | Mesh tab | Segmentation From Best-Fit Surfaces

### D1477

Mesh Analyze

### D1478

Evaluate and Repair (Evaluate and Repair)

### D1479

Design Mode | Mesh tab | Evaluate and Repair

### D1480

Face Info (Face Info)

### D1481

Design Mode | Mesh tab | Face Info

### D1482

Curvature Plot (Curvature Plot)

### D1483

Design Mode | Mesh tab | Curvature Plot

### D1484

Curvature Info (Curvature Info)

### D1485

Design Mode | Mesh tab | Curvature Info

### D1486

Evaluate Solid (Evaluate Solid)

### D1487

Design Mode | Mesh tab | Evaluate Solid

### D1488

Bounding Box Info (Bounding Box Info)

### D1489

Design Mode | Mesh tab | Bounding Box Info

### D1490

CAM

### D1491

OpenCAMLib 3D operations, experimental operations and CAMotics are conditional. Helpful Tools appears when experimental features are enabled.

### D1492

Project Setup

### D1493

New Job (New Job)

### D1494

CAM Mode | Home tab | New Job

### D1495

CAM Mode | Tools tab | New Job

### D1496

Work Plane (Work Plane)

### D1497

CAM Mode | Home tab | Work Plane

### D1498

CAM Mode | Tools tab | Work Plane

### D1499

Sanity Check (Sanity Check)

### D1500

CAM Mode | Tools tab | Sanity Check

### D1501

Post-processing (dropdown) (Post Process)

### D1502

CAM Mode | Tools tab | Post Process

### D1503

Post Process (Post Process)

### D1504

CAM Mode | Tools tab | Post Process > Post Process

### D1505

Post Process Selected Operations (Post Process Selected)

### D1506

CAM Mode | Tools tab | Post Process > Post Process Selected

### D1507

Tool Commands

### D1508

Simulators (dropdown) (CAM Simulator)

### D1509

CAM Mode | Tools tab | CAM Simulator

### D1510

CAM Simulator (CAM Simulator)

### D1511

CAM Mode | Tools tab | CAM Simulator > CAM Simulator

### D1512

Legacy CAM Simulator (Legacy CAM Simulator)

### D1513

CAM Mode | Tools tab | CAM Simulator > Legacy CAM Simulator

### D1514

Inspect Toolpath (Inspect Toolpath)

### D1515

CAM Mode | Tools tab | Inspect Toolpath

### D1516

Finish Selecting Loop (Finish Selecting Loop)

### D1517

CAM Mode | Tools tab | Finish Selecting Loop

### D1518

Toggle Operation (Toggle Operation)

### D1519

CAM Mode | Tools tab | Toggle Operation

### D1520

Add Toolbitâ€¦ (Add Toolbit)

### D1521

CAM Mode | Tools tab | Add Toolbit

### D1522

CAMotics Simulation (optional integration) (missing)

### D1523

New Operations

### D1524

Profile (Profile)

### D1525

CAM Mode | Tools tab | Profile

### D1526

Pocket Shape (Pocket Shape)

### D1527

CAM Mode | Tools tab | Pocket Shape

### D1528

Mill Facing (Mill Facing)

### D1529

CAM Mode | Tools tab | Mill Facing

### D1530

Helix (Helix)

### D1531

CAM Mode | Tools tab | Helix

### D1532

Adaptive (Adaptive)

### D1533

CAM Mode | Tools tab | Adaptive

### D1534

Slot (Slot)

### D1535

CAM Mode | Tools tab | Slot

### D1536

Drilling Operations (dropdown) (Drilling)

### D1537

CAM Mode | Tools tab | Drilling

### D1538

Drilling (Drilling)

### D1539

CAM Mode | Tools tab | Drilling > Drilling

### D1540

Thread Milling (Thread Milling)

### D1541

CAM Mode | Tools tab | Drilling > Thread Milling

### D1542

Engraving Operations (dropdown) (Engrave)

### D1543

CAM Mode | Tools tab | Engrave

### D1544

Engrave (Engrave)

### D1545

CAM Mode | Tools tab | Engrave > Engrave

### D1546

Deburr (Deburr)

### D1547

CAM Mode | Tools tab | Engrave > Deburr

### D1548

V-Carve (Vcarve)

### D1549

CAM Mode | Tools tab | Engrave > Vcarve

### D1550

Flute (experimental) (missing)

### D1551

3D Operations (dropdown) (missing)

### D1552

3D Pocket (missing)

### D1553

3D Surface (OpenCAMLib) (missing)

### D1554

Waterline (OpenCAMLib) (missing)

### D1555

Planar Surface (OpenCAMLib and experimental) (Parallel / Waterline)

### D1556

CAM Mode | Tools tab | Parallel / Waterline

### D1557

Rotary Surface (OpenCAMLib and experimental) (missing)

### D1558

Path Modification

### D1559

Copy Operation (Copy Operation)

### D1560

CAM Mode | Tools tab | Copy Operation

### D1561

Array (Array)

### D1562

CAM Mode | Tools tab | Array

### D1563

Simple Copy (Simple Copy)

### D1564

CAM Mode | Tools tab | Simple Copy

### D1565

Dress-up Operations (dropdown) (Array)

### D1566

CAM Mode | Tools tab | Array

### D1567

Array Dress-up (Array)

### D1568

CAM Mode | Tools tab | Array > Array

### D1569

Axis Mapping Dress-up (Axis Map)

### D1570

CAM Mode | Tools tab | Array > Axis Map

### D1571

Boundary Dress-up (Boundary)

### D1572

CAM Mode | Tools tab | Array > Boundary

### D1573

Boundary Dress-up (new version) (Boundary2)

### D1574

CAM Mode | Tools tab | Array > Boundary2

### D1575

Dogbone Dress-up (Dogbone)

### D1576

CAM Mode | Tools tab | Array > Dogbone

### D1577

Drag Knife Dress-up (Drag Knife)

### D1578

CAM Mode | Tools tab | Array > Drag Knife

### D1579

Lead In/Out Dress-up (Lead In/Out)

### D1580

CAM Mode | Tools tab | Array > Lead In/Out

### D1581

Mirror Dress-up (Mirror)

### D1582

CAM Mode | Tools tab | Array > Mirror

### D1583

Plunge Milling Dress-up (Plunge Milling)

### D1584

CAM Mode | Tools tab | Array > Plunge Milling

### D1585

Ramp Entry Dress-up (Ramp Entry)

### D1586

CAM Mode | Tools tab | Array > Ramp Entry

### D1587

Holding Tags Dress-up (Tag)

### D1588

CAM Mode | Tools tab | Array > Tag

### D1589

Z Correction Dress-up (Z Depth Correction)

### D1590

CAM Mode | Tools tab | Array > Z Depth Correction

### D1591

Helpful Tools (experimental)

### D1592

Area (experimental) (missing)

### D1593

Area Workplane (experimental) (missing)

### D1594

BIM

### D1595

Drafting Tools

### D1596

New Sketch (missing)

### D1597

Line (Line)

### D1598

Draft Mode | Home tab | Line

### D1599

Draft Mode | Tools tab | Line

### D1600

Polyline (Polyline)

### D1601

Draft Mode | Home tab | Polyline

### D1602

Draft Mode | Tools tab | Polyline

### D1603

Rectangle (Rectangle)

### D1604

Draft Mode | Tools tab | Rectangle

### D1605

Arc Tools (dropdown) (missing)

### D1606

Arc (Arc)

### D1607

Draft Mode | Tools tab | Arc > Arc

### D1608

Arc From 3 Points (Arc From 3 Points)

### D1609

Draft Mode | Tools tab | Arc > Arc From 3 Points

### D1610

Circle (Circle)

### D1611

Draft Mode | Tools tab | Circle

### D1612

Ellipse (Ellipse)

### D1613

Draft Mode | Tools tab | Ellipse

### D1614

Polygon (Polygon)

### D1615

Draft Mode | Tools tab | Polygon

### D1616

Spline Tools (dropdown) (missing)

### D1617

B-Spline (B-Spline)

### D1618

Draft Mode | Tools tab | B-Spline

### D1619

BÃ©zier Curve (BÃ©zier Curve)

### D1620

Draft Mode | Tools tab | Cubic BÃ©zier Curve > BÃ©zier Curve

### D1621

Cubic BÃ©zier Curve (Cubic BÃ©zier Curve)

### D1622

Draft Mode | Tools tab | Cubic BÃ©zier Curve > Cubic BÃ©zier Curve

### D1623

Point (Point)

### D1624

Draft Mode | Tools tab | Point

### D1625

Fillet (Fillet)

### D1626

Draft Mode | Home tab | Fillet

### D1627

Draft Mode | Tools tab | Fillet

### D1628

Draft Snap

### D1629

Snap Lock (Snap Lock)

### D1630

Draft Mode | Tools tab | Snap Lock

### D1631

Snap Endpoint (Snap Endpoint)

### D1632

Draft Mode | Tools tab | Snap Endpoint

### D1633

Snap Midpoint (Snap Midpoint)

### D1634

Draft Mode | Tools tab | Snap Midpoint

### D1635

Snap Center (Snap Center)

### D1636

Draft Mode | Tools tab | Snap Center

### D1637

Snap Angle (Snap Angle)

### D1638

Draft Mode | Tools tab | Snap Angle

### D1639

Snap Intersection (Snap Intersection)

### D1640

Draft Mode | Tools tab | Snap Intersection

### D1641

Snap Perpendicular (Snap Perpendicular)

### D1642

Draft Mode | Tools tab | Snap Perpendicular

### D1643

Snap Extension (Snap Extension)

### D1644

Draft Mode | Tools tab | Snap Extension

### D1645

Snap Parallel (Snap Parallel)

### D1646

Draft Mode | Tools tab | Snap Parallel

### D1647

Snap Special (Snap Special)

### D1648

Draft Mode | Tools tab | Snap Special

### D1649

Snap Near (Snap Near)

### D1650

Draft Mode | Tools tab | Snap Near

### D1651

Snap Ortho (Snap Ortho)

### D1652

Draft Mode | Tools tab | Snap Ortho

### D1653

Snap Grid (Snap Grid)

### D1654

Draft Mode | Tools tab | Snap Grid

### D1655

Snap Working Plane (Snap Working Plane)

### D1656

Draft Mode | Tools tab | Snap Working Plane

### D1657

Snap Dimensions (Snap Dimensions)

### D1658

Draft Mode | Tools tab | Snap Dimensions

### D1659

Toggle Grid (Toggle Grid)

### D1660

Draft Mode | Tools tab | Toggle Grid

### D1661

3D/BIM Tools

### D1662

Site (missing)

### D1663

Building (missing)

### D1664

Level (missing)

### D1665

Space (missing)

### D1666

Wall (missing)

### D1667

Curtain Wall (missing)

### D1668

Column (missing)

### D1669

Beam (missing)

### D1670

Slab (missing)

### D1671

Door (missing)

### D1672

Window (missing)

### D1673

Covering (missing)

### D1674

Pipe (missing)

### D1675

Connector (missing)

### D1676

Stairs (missing)

### D1677

Roof (missing)

### D1678

Panel (missing)

### D1679

Frame (missing)

### D1680

Fence (missing)

### D1681

Truss (missing)

### D1682

Equipment (missing)

### D1683

Custom Rebar (missing)

### D1684

Generic 3D Tools (dropdown) (missing)

### D1685

Profile (missing)

### D1686

Box (missing)

### D1687

Shape Builder (missing)

### D1688

Facebinder (Facebinder)

### D1689

Draft Mode | Tools tab | Facebinder

### D1690

Objects Library (missing)

### D1691

Component (missing)

### D1692

Reference (missing)

### D1693

Annotation Tools

### D1694

Aligned Dimension (missing)

### D1695

Horizontal Dimension (missing)

### D1696

Vertical Dimension (missing)

### D1697

Text (missing)

### D1698

Leader (missing)

### D1699

Label (Label)

### D1700

Draft Mode | Tools tab | Label

### D1701

Hatch (Hatch)

### D1702

Draft Mode | Tools tab | Hatch

### D1703

Axis Tools (dropdown) (missing)

### D1704

Axis (missing)

### D1705

Axis System (missing)

### D1706

Grid (missing)

### D1707

Section Plane (missing)

### D1708

Create 2D Views (dropdown) (missing)

### D1709

2D Drawing (missing)

### D1710

Section View (missing)

### D1711

Section Cut (missing)

### D1712

Update Shape 2D View (missing)

### D1713

New Page (missing)

### D1714

New View (missing)

### D1715

General Tools

### D1716

Move (Move)

### D1717

Draft Mode | Tools tab | Move

### D1718

Rotate (Rotate)

### D1719

Draft Mode | Tools tab | Rotate

### D1720

Scale (Scale)

### D1721

Draft Mode | Tools tab | Scale

### D1722

Mirror (Mirror)

### D1723

Draft Mode | Tools tab | Mirror

### D1724

Cloning Tools (dropdown) (missing)

### D1725

Clone (missing)

### D1726

Make Link (missing)

### D1727

Unclone (missing)

### D1728

Copy (missing)

### D1729

Simple Copy (missing)

### D1730

Compound (missing)

### D1731

2D Tools

### D1732

Offset Tools (dropdown) (missing)

### D1733

2D Offset (missing)

### D1734

Offset (Offset)

### D1735

Draft Mode | Tools tab | Offset

### D1736

Trimex (missing)

### D1737

Join (Join)

### D1738

Draft Mode | Tools tab | Join

### D1739

Split (Split)

### D1740

Draft Mode | Tools tab | Split

### D1741

Stretch (Stretch)

### D1742

Draft Mode | Tools tab | Stretch

### D1743

Draft to Sketch (Draft to Sketch)

### D1744

Draft Mode | Tools tab | Draft to Sketch

### D1745

Edit (Edit)

### D1746

Draft Mode | Tools tab | Edit

### D1747

Object Tools

### D1748

Upgrade (Upgrade)

### D1749

Draft Mode | Tools tab | Upgrade

### D1750

Downgrade (Downgrade)

### D1751

Draft Mode | Tools tab | Downgrade

### D1752

Add Component (missing)

### D1753

Remove Component (missing)

### D1754

3D Tools

### D1755

Array Tools (dropdown) (missing)

### D1756

Array (Array)

### D1757

Draft Mode | Tools tab | Array > Array

### D1758

Path Link Array (Path Link Array)

### D1759

Draft Mode | Tools tab | Array > Path Link Array

### D1760

Polar Array (Polar Array)

### D1761

Draft Mode | Tools tab | Array > Polar Array

### D1762

Point Link Array (Point Link Array)

### D1763

Draft Mode | Tools tab | Array > Point Link Array

### D1764

Cut With Plane (missing)

### D1765

Extrude (missing)

### D1766

Extrude Face (missing)

### D1767

Boolean Tools (dropdown) (missing)

### D1768

Union (missing)

### D1769

Difference (missing)

### D1770

Intersection (missing)

### D1771

Manage Tools

### D1772

BIM Setup (missing)

### D1773

Setup Project (missing)

### D1774

Manage Doors and Windows (missing)

### D1775

IFC Management (dropdown) (missing)

### D1776

IFC Elements (missing)

### D1777

IFC Quantities (missing)

### D1778

IFC Properties (missing)

### D1779

Classification (missing)

### D1780

Manage Layers (missing)

### D1781

Material (missing)

### D1782

Report Tools (dropdown) (missing)

### D1783

Report (missing)

### D1784

Schedule (missing)

### D1785

Survey (missing)

### D1786

Preflight Checks (missing)

### D1787

Annotation Styles (Annotation Styles)

### D1788

Draft Mode | Tools tab | Annotation Styles

### D1789

FEM

### D1790

FEM source toolbars are included even when FEM is not enabled in a build. VTK result filters and solver choices depend on compiled support and installed solvers.

### D1791

Model

### D1792

New Analysis (missing)

### D1793

Solid Material (missing)

### D1794

Fluid Material (missing)

### D1795

Non-Linear Mechanical Material (missing)

### D1796

Reinforced Material (Concrete) (missing)

### D1797

Material Editor (missing)

### D1798

Beam Cross Section (missing)

### D1799

Beam Rotation (missing)

### D1800

Shell Plate Thickness (missing)

### D1801

Fluid Section for 1D Flow (missing)

### D1802

Electromagnetic Boundary Conditions

### D1803

Electromagnetic Constraints (dropdown) (missing)

### D1804

Electromagnetic Boundary Condition (missing)

### D1805

Current Density Boundary Condition (missing)

### D1806

Magnetization Boundary Condition (missing)

### D1807

Electric Charge Density (missing)

### D1808

Fluid Boundary Conditions

### D1809

Initial Flow Velocity Condition (missing)

### D1810

Initial Pressure Condition (missing)

### D1811

Flow Velocity Boundary Condition (missing)

### D1812

Geometrical Analysis Features

### D1813

Plane Multi-Point Constraint (missing)

### D1814

Section Print Feature (missing)

### D1815

Local Coordinate System (missing)

### D1816

Mechanical Boundary Conditions and Loads

### D1817

Fixed Boundary Condition (missing)

### D1818

Rigid Body Constraint (missing)

### D1819

Displacement Boundary Condition (missing)

### D1820

Contact Constraint (missing)

### D1821

Tie Constraint (missing)

### D1822

Spring Boundary Condition (missing)

### D1823

Force Load (missing)

### D1824

Pressure Load (missing)

### D1825

Centrifugal Load (missing)

### D1826

Gravity Load (missing)

### D1827

Thermal Boundary Conditions and Loads

### D1828

Initial Temperature (missing)

### D1829

Heat Flux Load (missing)

### D1830

Temperature Boundary Condition (missing)

### D1831

Body Heat Source (missing)

### D1832

Mesh

### D1833

Mesh From Shape by Netgen (missing)

### D1834

Mesh From Shape by Gmsh (missing)

### D1835

Mesh Refinement (missing)

### D1836

Mesh Group (missing)

### D1837

GMSH Refinements (missing)

### D1838

FEM Mesh to Mesh (missing)

### D1839

Solve

### D1840

Solvers (dropdown) (missing)

### D1841

CalculiX Solver (missing)

### D1842

Elmer Solver (missing)

### D1843

Mystran Solver (missing)

### D1844

Z88 Solver (missing)

### D1845

Mechanical Equations (dropdown) (missing)

### D1846

Elasticity Equation (missing)

### D1847

Deformation Equation (missing)

### D1848

Electromagnetic Equations (dropdown) (missing)

### D1849

Electrostatic Equation (missing)

### D1850

Electricforce Equation (missing)

### D1851

Magnetodynamic Equation (missing)

### D1852

Magnetodynamic 2D Equation (missing)

### D1853

Static Current Equation (missing)

### D1854

Flow Equation (missing)

### D1855

Flux Equation (missing)

### D1856

Heat Equation (missing)

### D1857

Solver Job Control (missing)

### D1858

Run Solver (missing)

### D1859

Results

### D1860

Purge Results (missing)

### D1861

Show Result (missing)

### D1862

Apply Changes to Pipeline (missing)

### D1863

Post Pipeline From Result (missing)

### D1864

Pipeline Branch (missing)

### D1865

Warp Filter (missing)

### D1866

Scalar Clip Filter (missing)

### D1867

Function Cut Filter (missing)

### D1868

Region Clip Filter (missing)

### D1869

Contours Filter (missing)

### D1870

Glyph Filter (missing)

### D1871

Line Clip Filter (missing)

### D1872

Stress Linearization Plot (missing)

### D1873

Data at Point Clip Filter (missing)

### D1874

Calculator Filter (missing)

### D1875

Filter Functions (dropdown) (missing)

### D1876

Plane (missing)

### D1877

Sphere (missing)

### D1878

Cylinder (missing)

### D1879

Box (missing)

### D1880

Data Visualizations (dropdown) (missing)

### D1881

Line Plot (missing)

### D1882

Histogram (missing)

### D1883

Data Table (missing)

### D1884

Utilities

### D1885

Clipping Plane on Face (missing)

### D1886

Remove All Clipping Planes (missing)

### D1887

FEM Examples (missing)

### D1888

Inspection

### D1889

Inspection

### D1890

Visual Inspection (missing)

### D1891

Inspectionâ€¦ (missing)

### D1892

Material

### D1893

Material

### D1894

Edit (Edit)

### D1895

Material Mode | Home tab | Edit

### D1896

Material Mode | Tools tab | Edit

### D1897

OpenSCAD

### D1898

Add OpenSCAD Element, Mesh Boolean, Hull and Minkowski Sum require a configured OpenSCAD executable.

### D1899

OpenSCAD Tools

### D1900

Replace Object (missing)

### D1901

Remove Objects and Children (missing)

### D1902

Explode Group (missing)

### D1903

Refine Shape Feature (missing)

### D1904

Increase Tolerance Feature (missing)

### D1905

Add OpenSCAD Element (missing)

### D1906

Mesh Boolean (missing)

### D1907

Hull (missing)

### D1908

Minkowski Sum (missing)

### D1909

Frequently-used Part WB tools

### D1910

Check Geometry (Check Geometry)

### D1911

Part Mode | Tools tab | Check Geometry

### D1912

Primitive (Primitive)

### D1913

Part Mode | Tools tab | Primitive

### D1914

Shape Builder (Shape Builder)

### D1915

Part Mode | Tools tab | Shape Builder

### D1916

Cut (Cut)

### D1917

Part Mode | Tools tab | Cut

### D1918

Union (Union)

### D1919

Part Mode | Tools tab | Union

### D1920

Intersection (Intersection)

### D1921

Part Mode | Tools tab | Intersection

### D1922

Extrude (Extrude)

### D1923

Part Mode | Tools tab | Extrude

### D1924

Revolve (Revolve)

### D1925

Part Mode | Tools tab | Revolve

### D1926

Points

### D1927

Points Tools

### D1928

Import Pointsâ€¦ (missing)

### D1929

Export Pointsâ€¦ (missing)

### D1930

Convert to Points (missing)

### D1931

Structured Point Cloud (missing)

### D1932

Merge Point Clouds (missing)

### D1933

Cut Point Cloud (missing)

### D1934

Reverse Engineering

### D1935

Reverse Engineering

### D1936

Approximate B-Spline Surfaceâ€¦ (missing)

### D1937

Spreadsheet

### D1938

Spreadsheet

### D1939

New Spreadsheet (New Spreadsheet)

### D1940

Spreadsheet Mode | Home tab | New Spreadsheet

### D1941

Spreadsheet Mode | Tools tab | New Spreadsheet

### D1942

Import Spreadsheet (Import Spreadsheet)

### D1943

Spreadsheet Mode | Home tab | Import Spreadsheet

### D1944

Spreadsheet Mode | Tools tab | Import Spreadsheet

### D1945

Export Spreadsheet (Export Spreadsheet)

### D1946

Spreadsheet Mode | Home tab | Export Spreadsheet

### D1947

Spreadsheet Mode | Tools tab | Export Spreadsheet

### D1948

Merge Cells (Merge Cells)

### D1949

Spreadsheet Mode | Tools tab | Merge Cells

### D1950

Split Cell (Split Cell)

### D1951

Spreadsheet Mode | Tools tab | Split Cell

### D1952

Align Left (Align Left)

### D1953

Spreadsheet Mode | Tools tab | Align Left

### D1954

Align Horizontal Center (Align Horizontal Center)

### D1955

Spreadsheet Mode | Tools tab | Align Horizontal Center

### D1956

Align Right (Align Right)

### D1957

Spreadsheet Mode | Tools tab | Align Right

### D1958

Align Top (Align Top)

### D1959

Spreadsheet Mode | Tools tab | Align Top

### D1960

Align Vertical Center (Align Vertical Center)

### D1961

Spreadsheet Mode | Tools tab | Align Vertical Center

### D1962

Align Bottom (Align Bottom)

### D1963

Spreadsheet Mode | Tools tab | Align Bottom

### D1964

Bold Text (Bold Text)

### D1965

Spreadsheet Mode | Tools tab | Bold Text

### D1966

Italic Text (Italic Text)

### D1967

Spreadsheet Mode | Tools tab | Italic Text

### D1968

Underline Text (Underline Text)

### D1969

Spreadsheet Mode | Tools tab | Underline Text

### D1970

Set Alias (Set Alias)

### D1971

Spreadsheet Mode | Tools tab | Set Alias

### D1972

Tech Draw

### D1973

TechDraw Pages

### D1974

New Page (New Page)

### D1975

Drawing Mode | Home tab | New Page

### D1976

Drawing Mode | Tools tab | New Page

### D1977

New Page From Template (New Page From Template)

### D1978

Drawing Mode | Home tab | New Page From Template

### D1979

Drawing Mode | Tools tab | New Page From Template

### D1980

Update Template Fields (Update Template Fields)

### D1981

Drawing Mode | Home tab | Update Template Fields

### D1982

Drawing Mode | Tools tab | Update Template Fields

### D1983

Redraw Page (Redraw Page)

### D1984

Drawing Mode | Tools tab | Redraw Page

### D1985

Print All Pages (Print All Pages)

### D1986

Drawing Mode | Tools tab | Print All Pages

### D1987

TechDraw Views

### D1988

New View (New View)

### D1989

Drawing Mode | Tools tab | New View

### D1990

Broken View (Broken View)

### D1991

Drawing Mode | Tools tab | Broken View

### D1992

Active View (Active View)

### D1993

Drawing Mode | Tools tab | Active View

### D1994

Section View (dropdown) (Section View)

### D1995

Drawing Mode | Tools tab | Section View

### D1996

Section View (Section View)

### D1997

Drawing Mode | Tools tab | Section View > Section View

### D1998

Complex Section View (Complex Section View)

### D1999

Drawing Mode | Tools tab | Section View > Complex Section View

### D2000

Detail View (Detail View)

### D2001

Drawing Mode | Tools tab | Detail View

### D2002

Draft View (Draft View)

### D2003

Drawing Mode | Tools tab | Draft View

### D2004

Spreadsheet View (Spreadsheet View)

### D2005

Drawing Mode | Tools tab | Spreadsheet View

### D2006

Clip Group (Clip Group)

### D2007

Drawing Mode | Tools tab | Clip Group

### D2008

TechDraw Stacking

### D2009

Stack Top (dropdown) (Stack Top)

### D2010

Drawing Mode | Tools tab | Stack Top

### D2011

Stack Top (Stack Top)

### D2012

Drawing Mode | Tools tab | Stack Top > Stack Top

### D2013

Stack Bottom (Stack Bottom)

### D2014

Drawing Mode | Tools tab | Stack Top > Stack Bottom

### D2015

Stack Up (Stack Up)

### D2016

Drawing Mode | Tools tab | Stack Top > Stack Up

### D2017

Stack Down (Stack Down)

### D2018

Drawing Mode | Tools tab | Stack Top > Stack Down

### D2019

TechDraw Dimensions

### D2020

Dimension (Dimension)

### D2021

Drawing Mode | Tools tab | Dimension > Dimension

### D2022

Dimension (dropdown) (Dimension)

### D2023

Drawing Mode | Tools tab | Dimension

### D2024

Dimension (Dimension)

### D2025

Drawing Mode | Tools tab | Dimension > Dimension

### D2026

Length Dimension (Length Dimension)

### D2027

Drawing Mode | Tools tab | Dimension > Length Dimension

### D2028

Horizontal Length Dimension (Horizontal Length Dimension)

### D2029

Drawing Mode | Tools tab | Dimension > Horizontal Length Dimension

### D2030

Vertical Length Dimension (Vertical Length Dimension)

### D2031

Drawing Mode | Tools tab | Dimension > Vertical Length Dimension

### D2032

Radius Dimension (Radius Dimension)

### D2033

Drawing Mode | Tools tab | Dimension > Radius Dimension

### D2034

Diameter Dimension (Diameter Dimension)

### D2035

Drawing Mode | Tools tab | Dimension > Diameter Dimension

### D2036

Angle Dimension (Angle Dimension)

### D2037

Drawing Mode | Tools tab | Dimension > Angle Dimension

### D2038

Angle Dimension From 3 Points (Angle Dimension From 3 Points)

### D2039

Drawing Mode | Tools tab | Dimension > Angle Dimension From 3 Points

### D2040

Area Annotation (Area Annotation)

### D2041

Drawing Mode | Tools tab | Dimension > Area Annotation

### D2042

Arc Length Dimension (Arc Length Dimension)

### D2043

Drawing Mode | Tools tab | Dimension > Arc Length Dimension

### D2044

Horizontal Extent Dimension (Horizontal Extent Dimension)

### D2045

Drawing Mode | Tools tab | Dimension > Horizontal Extent Dimension

### D2046

Vertical Extent Dimension (Vertical Extent Dimension)

### D2047

Drawing Mode | Tools tab | Dimension > Vertical Extent Dimension

### D2048

Horizontal Chain Dimension (Horizontal Chain Dimension)

### D2049

Drawing Mode | Tools tab | Dimension > Horizontal Chain Dimension

### D2050

Vertical Chain Dimension (Vertical Chain Dimension)

### D2051

Drawing Mode | Tools tab | Dimension > Vertical Chain Dimension

### D2052

Oblique Chain Dimension (Oblique Chain Dimension)

### D2053

Drawing Mode | Tools tab | Dimension > Oblique Chain Dimension

### D2054

Horizontal Coordinate Dimension (Horizontal Coordinate Dimension)

### D2055

Drawing Mode | Tools tab | Dimension > Horizontal Coordinate Dimension

### D2056

Vertical Coordinate Dimension (Vertical Coordinate Dimension)

### D2057

Drawing Mode | Tools tab | Dimension > Vertical Coordinate Dimension

### D2058

Oblique Coordinate Dimension (Oblique Coordinate Dimension)

### D2059

Drawing Mode | Tools tab | Dimension > Oblique Coordinate Dimension

### D2060

Horizontal Chamfer Dimension (Horizontal Chamfer Dimension)

### D2061

Drawing Mode | Tools tab | Dimension > Horizontal Chamfer Dimension

### D2062

Vertical Chamfer Dimension (Vertical Chamfer Dimension)

### D2063

Drawing Mode | Tools tab | Dimension > Vertical Chamfer Dimension

### D2064

Length Dimension (Length Dimension)

### D2065

Drawing Mode | Tools tab | Dimension > Length Dimension

### D2066

Horizontal Length Dimension (Horizontal Length Dimension)

### D2067

Drawing Mode | Tools tab | Dimension > Horizontal Length Dimension

### D2068

Vertical Length Dimension (Vertical Length Dimension)

### D2069

Drawing Mode | Tools tab | Dimension > Vertical Length Dimension

### D2070

Radius Dimension (Radius Dimension)

### D2071

Drawing Mode | Tools tab | Dimension > Radius Dimension

### D2072

Diameter Dimension (Diameter Dimension)

### D2073

Drawing Mode | Tools tab | Dimension > Diameter Dimension

### D2074

Angle Dimension (Angle Dimension)

### D2075

Drawing Mode | Tools tab | Dimension > Angle Dimension

### D2076

Angle Dimension From 3 Points (Angle Dimension From 3 Points)

### D2077

Drawing Mode | Tools tab | Dimension > Angle Dimension From 3 Points

### D2078

Area Annotation (Area Annotation)

### D2079

Drawing Mode | Tools tab | Dimension > Area Annotation

### D2080

Horizontal extent (dropdown) (missing)

### D2081

Horizontal extent (Horizontal Extent Dimension)

### D2082

Drawing Mode | Tools tab | Dimension > Horizontal Extent Dimension

### D2083

Vertical extent (Vertical Extent Dimension)

### D2084

Drawing Mode | Tools tab | Dimension > Vertical Extent Dimension

### D2085

Balloon Annotation (Balloon Annotation)

### D2086

Drawing Mode | Tools tab | Balloon Annotation

### D2087

Axonometric Length Dimension (Axonometric Length Dimension)

### D2088

Drawing Mode | Tools tab | Axonometric Length Dimension

### D2089

Repair Dimension References (Repair Dimension References)

### D2090

Drawing Mode | Tools tab | Repair Dimension References

### D2091

TechDraw Attributes

### D2092

Select Line Attributes, Cascade Spacing and Delta Distance (Select Line Attributes, Cascade Spacing and Delta Distance)

### D2093

Drawing Mode | Tools tab | Select Line Attributes, Cascade Spacing and Delta Distance

### D2094

Change Line Attributes (Change Line Attributes)

### D2095

Drawing Mode | Tools tab | Change Line Attributes

### D2096

Extend Line (dropdown) (Extend Line)

### D2097

Drawing Mode | Tools tab | Extend Line

### D2098

Extend Line (Extend Line)

### D2099

Drawing Mode | Tools tab | Extend Line > Extend Line

### D2100

Shorten Line (Shorten Line)

### D2101

Drawing Mode | Tools tab | Extend Line > Shorten Line

### D2102

Toggle View Lock (Toggle View Lock)

### D2103

Drawing Mode | Tools tab | Toggle View Lock

### D2104

Position Section View (Position Section View)

### D2105

Drawing Mode | Tools tab | Position Section View

### D2106

Area Annotation (missing)

### D2107

Arc Length Annotation (missing)

### D2108

Customize Format Label (Customize Format Label)

### D2109

Drawing Mode | Tools tab | Customize Format Label

### D2110

TechDraw Centerlines

### D2111

Circle Centerlines (dropdown) (Circle Centerlines)

### D2112

Drawing Mode | Tools tab | Circle Centerlines

### D2113

Circle Centerlines (Circle Centerlines)

### D2114

Drawing Mode | Tools tab | Circle Centerlines > Circle Centerlines

### D2115

Bolt Circle Centerlines (Bolt Circle Centerlines)

### D2116

Drawing Mode | Tools tab | Circle Centerlines > Bolt Circle Centerlines

### D2117

Cosmetic Thread Hole Side View (dropdown) (Cosmetic Thread Hole Side View)

### D2118

Drawing Mode | Tools tab | Cosmetic Thread Hole Side View

### D2119

Cosmetic Thread Hole Side View (Cosmetic Thread Hole Side View)

### D2120

Drawing Mode | Tools tab | Cosmetic Thread Hole Side View > Cosmetic Thread Hole Side View

### D2121

Cosmetic Thread Hole Bottom View (Cosmetic Thread Hole Bottom View)

### D2122

Drawing Mode | Tools tab | Cosmetic Thread Hole Side View > Cosmetic Thread Hole Bottom View

### D2123

Cosmetic Thread Bolt Side View (Cosmetic Thread Bolt Side View)

### D2124

Drawing Mode | Tools tab | Cosmetic Thread Hole Side View > Cosmetic Thread Bolt Side View

### D2125

Cosmetic Thread Bolt Bottom View (Cosmetic Thread Bolt Bottom View)

### D2126

Drawing Mode | Tools tab | Cosmetic Thread Hole Side View > Cosmetic Thread Bolt Bottom View

### D2127

Cosmetic Intersection Vertices (dropdown) (Cosmetic Intersection Vertices)

### D2128

Drawing Mode | Tools tab | Cosmetic Intersection Vertices

### D2129

Cosmetic Intersection Vertices (Cosmetic Intersection Vertices)

### D2130

Drawing Mode | Tools tab | Cosmetic Intersection Vertices > Cosmetic Intersection Vertices

### D2131

Offset Vertex (Offset Vertex)

### D2132

Drawing Mode | Tools tab | Cosmetic Intersection Vertices > Offset Vertex

### D2133

Cosmetic 1 Point Circle (dropdown) (Cosmetic 1 Point Circle)

### D2134

Drawing Mode | Tools tab | Cosmetic 1 Point Circle

### D2135

Cosmetic 1 Point Circle (Cosmetic 1 Point Circle)

### D2136

Drawing Mode | Tools tab | Cosmetic 1 Point Circle > Cosmetic 1 Point Circle

### D2137

Cosmetic 2 Point Circle (Cosmetic 2 Point Circle)

### D2138

Drawing Mode | Tools tab | Cosmetic 1 Point Circle > Cosmetic 2 Point Circle

### D2139

Cosmetic 3 Point Circle (Cosmetic 3 Point Circle)

### D2140

Drawing Mode | Tools tab | Cosmetic 1 Point Circle > Cosmetic 3 Point Circle

### D2141

Cosmetic Arc (Cosmetic Arc)

### D2142

Drawing Mode | Tools tab | Cosmetic 1 Point Circle > Cosmetic Arc

### D2143

Cosmetic Parallel Line (dropdown) (Cosmetic Parallel Line)

### D2144

Drawing Mode | Tools tab | Cosmetic Parallel Line

### D2145

Cosmetic Parallel Line (Cosmetic Parallel Line)

### D2146

Drawing Mode | Tools tab | Cosmetic Parallel Line > Cosmetic Parallel Line

### D2147

Cosmetic Perpendicular Line (Cosmetic Perpendicular Line)

### D2148

Drawing Mode | Tools tab | Cosmetic Parallel Line > Cosmetic Perpendicular Line

### D2149

TechDraw Extend Dimensions

### D2150

Horizontal Chain Dimension (dropdown) (missing)

### D2151

Horizontal Chain Dimension (Horizontal Chain Dimension)

### D2152

Drawing Mode | Tools tab | Dimension > Horizontal Chain Dimension

### D2153

Vertical Chain Dimension (Vertical Chain Dimension)

### D2154

Drawing Mode | Tools tab | Dimension > Vertical Chain Dimension

### D2155

Oblique Chain Dimension (Oblique Chain Dimension)

### D2156

Drawing Mode | Tools tab | Dimension > Oblique Chain Dimension

### D2157

Horizontal Coordinate Dimension (dropdown) (missing)

### D2158

Horizontal Coordinate Dimension (Horizontal Coordinate Dimension)

### D2159

Drawing Mode | Tools tab | Dimension > Horizontal Coordinate Dimension

### D2160

Vertical Coordinate Dimension (Vertical Coordinate Dimension)

### D2161

Drawing Mode | Tools tab | Dimension > Vertical Coordinate Dimension

### D2162

Oblique Coordinate Dimension (Oblique Coordinate Dimension)

### D2163

Drawing Mode | Tools tab | Dimension > Oblique Coordinate Dimension

### D2164

Horizontal Chamfer Dimension (dropdown) (missing)

### D2165

Horizontal Chamfer Dimension (Horizontal Chamfer Dimension)

### D2166

Drawing Mode | Tools tab | Dimension > Horizontal Chamfer Dimension

### D2167

Vertical Chamfer Dimension (Vertical Chamfer Dimension)

### D2168

Drawing Mode | Tools tab | Dimension > Vertical Chamfer Dimension

### D2169

Arc Length Dimension (Arc Length Dimension)

### D2170

Drawing Mode | Tools tab | Dimension > Arc Length Dimension

### D2171

Insert 'âŒ€' Prefix (dropdown) (Insert 'âŒ€' Prefix)Drawing Mode | Tools tab | Insert 'âŒ€' Prefix

### D2172

Insert 'âŒ€' Prefix (Insert 'âŒ€' Prefix)Drawing Mode | Tools tab | Insert 'âŒ€' Prefix > Insert 'âŒ€' Prefix

### D2173

Insert 'â–¡' Prefix (Insert 'âŒ€' Prefix)

### D2174

Drawing Mode | Tools tab | Insert 'âŒ€' Prefix > Insert 'âŒ€' Prefix

### D2175

Insert 'nÃ—' Prefix (Insert 'nÃ—' Prefix)

### D2176

Drawing Mode | Tools tab | Insert 'âŒ€' Prefix > Insert 'nÃ—' Prefix

### D2177

Remove Prefix (Remove Prefix)

### D2178

Drawing Mode | Tools tab | Insert 'âŒ€' Prefix > Remove Prefix

### D2179

Increase Decimal Places (dropdown) (Increase Decimal Places)

### D2180

Drawing Mode | Tools tab | Increase Decimal Places

### D2181

Increase Decimal Places (Increase Decimal Places)

### D2182

Drawing Mode | Tools tab | Increase Decimal Places > Increase Decimal Places

### D2183

Decrease Decimal Places (Decrease Decimal Places)

### D2184

Drawing Mode | Tools tab | Increase Decimal Places > Decrease Decimal Places

### D2185

TechDraw File Access

### D2186

Export Page as SVG (Export Page as SVG)

### D2187

Drawing Mode | Tools tab | Export Page as SVG

### D2188

Export Page as DXF (Export Page as DXF)

### D2189

Drawing Mode | Tools tab | Export Page as DXF

### D2190

TechDraw Decoration

### D2191

Toggle View Frames (Toggle View Frames)

### D2192

Drawing Mode | Tools tab | Toggle View Frames

### D2193

Image Hatch (Image Hatch)

### D2194

Drawing Mode | Tools tab | Image Hatch

### D2195

Geometric Hatch (Geometric Hatch)

### D2196

Drawing Mode | Tools tab | Geometric Hatch

### D2197

TechDraw Annotation

### D2198

Rich Text Annotation (Rich Text Annotation)

### D2199

Drawing Mode | Tools tab | Rich Text Annotation

### D2200

Leader Line (Leader Line)

### D2201

Drawing Mode | Tools tab | Leader Line

### D2202

Cosmetic Vertex (dropdown) (Cosmetic Vertex)

### D2203

Drawing Mode | Tools tab | Cosmetic Vertex

### D2204

Cosmetic Vertex (Cosmetic Vertex)

### D2205

Drawing Mode | Tools tab | Cosmetic Vertex > Cosmetic Vertex

### D2206

Midpoint Vertices (Midpoint Vertices)

### D2207

Drawing Mode | Tools tab | Cosmetic Vertex > Midpoint Vertices

### D2208

Quadrant Vertices (Quadrant Vertices)

### D2209

Drawing Mode | Tools tab | Cosmetic Vertex > Quadrant Vertices

### D2210

Centerline on Face (dropdown) (Centerline on Face)

### D2211

Drawing Mode | Tools tab | Centerline on Face

### D2212

Centerline on Face (Centerline on Face)

### D2213

Drawing Mode | Tools tab | Centerline on Face > Centerline on Face

### D2214

Centerline Between 2 Lines (Centerline Between 2 Lines)

### D2215

Drawing Mode | Tools tab | Centerline on Face > Centerline Between 2 Lines

### D2216

Centerline Between 2 Points (Centerline Between 2 Points)

### D2217

Drawing Mode | Tools tab | Centerline on Face > Centerline Between 2 Points

### D2218

Cosmetic Line Through 2 Points (Cosmetic Line Through 2 Points)

### D2219

Drawing Mode | Tools tab | Cosmetic Line Through 2 Points

### D2220

Edit Line Appearance (Edit Line Appearance)

### D2221

Drawing Mode | Tools tab | Edit Line Appearance

### D2222

Toggle Edge Visibility (Toggle Edge Visibility)

### D2223

Drawing Mode | Tools tab | Toggle Edge Visibility

### D2224

Weld Symbol (Weld Symbol)

### D2225

Drawing Mode | Tools tab | Weld Symbol

### D2226

Surface Finish Symbol (Surface Finish Symbol)

### D2227

Drawing Mode | Tools tab | Surface Finish Symbol

### D2228

Hole/Shaft Fit (Hole/Shaft Fit)

### D2229

Drawing Mode | Tools tab | Hole/Shaft Fit

### D2230

Test Framework

### D2231

TestTools

### D2232

Self-test... (Self-test)

### D2233

Test Framework Mode | Home tab | Self-test

### D2234

Test Framework Mode | Tools tab | Self-test

### D2235

Test all (Test all)

### D2236

Test Framework Mode | Home tab | Test all

### D2237

Test Framework Mode | Tools tab | Test all

### D2238

Test Document (Test Document)

### D2239

Test Framework Mode | Home tab | Test Document

### D2240

Test Framework Mode | Tools tab | Test Document

### D2241

Test base (Test base)

### D2242

Test Framework Mode | Tools tab | Test base

### D2243

MeshPart

### D2244

MeshPart

### D2245

Mesh From Shape (missing)

### D2246

Robot

### D2247

Robot

### D2248

Place Robot (missing)

### D2249

Trajectory (missing)

### D2250

Insert in Trajectory (missing)

### D2251

Insert in Trajectory (missing)

### D2252

Edge to Trajectory (missing)

### D2253

Dress-Up Trajectory (missing)

### D2254

Trajectory Compound (missing)

### D2255

Set Home Position (missing)

### D2256

Move to Home (missing)

### D2257

Simulate Trajectory (missing)

### D2258

Start supplies the Start page rather than a separate selectable workbench toolbar. Tux supplies navigation and toolbar services rather than a separate workbench. Import/export, Help, Measure and Addon Manager supply shared commands or services rather than additional workbench toolbar groups in this baseline.

### D2259

Plus Toolbars

### D2260

Use a mode selector in the upper left of the toolbar section. Include Design, Draft and CAM, with FEM and 3D printing modes when those workbenches are available.

### D2261

Provide a common horizontal toolbar above the ribbon for all modes.

### D2262

File: New File, Open, Save and Save As, all small icons. New File uses the native New Document icon and the caption New File.

### D2263

Edit: Undo, Redo and Recompute, all small icons.

### D2264

Clipboard: Cut, Copy and Paste, all small icons.

### D2265

Apply the same button hierarchy to all future UI modifications.

### D2266

Full size: the most commonly used primary operations, such as Extrude and Revolve, in one row.

### D2267

Medium: 32 logical pixel ribbon icons in 42-pixel-high buttons, arranged in two rows with native tooltips and accessible names.

### D2268

Small: secondary actions without visible name text, arranged in three rows with as many columns as needed.

### D2269

Dropdown: uses same size icons as small icons and has extra width for the drop down arrow. less frequently used choices grouped behind a common action. Auto Dimension offers vertical, horizontal, angle, radius and diameter constraints.

### D2270

Use a consistent grid with gray vertical line dividers between adjacent groups on every tab. Show complete large-button and group captions on up to two lines as needed; grow width/height rather than abbreviating or cutting off text. Medium and small buttons show icons only, with native hover tooltips and accessible names retained.

### D2271

Keep TOOLBARS.md organized by Classic workbench and toolbar, then Plus mode, tab and section, with button sizes and consolidations recorded. Use one command per Classic row and small icon illustrations; retain the command-function catalog at the end.

### D2272

Design Mode

### D2273

Current Plus configuration: tabs and groups are listed left to right; button clusters are listed by column, top to bottom. Large buttons occupy a full column, medium clusters use two rows, and small clusters use three rows. File, Edit and Clipboard remain in the separate common toolbar. Native actions, enablement, shortcuts, Classic preferences and modeling behavior are retained. Tab in Primitives is disabled because it is not implemented. Medium and small buttons show icons only. Gray vertical dividers separate adjacent groups. Large-button and group captions retain their complete text on up to two lines; sizing grows as needed. Modeling follows the revised six-group outline below; Pipe remains a native command outside this tab.

### D2274

Home Tab

### D2275

Main group:

### D2276

Medium Button Cluster

### D2277

New Component

### D2278

Add Component

### D2279

Modeling group:

### D2280

Extrude (Large Button)

### D2281

Revolve (Large Button)

### D2282

Medium Button Cluster

### D2283

Fillet/Chamfer (Medium Button Dropdown)

### D2284

Fillet

### D2285

Chamfer

### D2286

Sketch group:

### D2287

Medium Button Cluster

### D2288

New Sketch

### D2289

Coordinate System (Medium Button Dropdown)

### D2290

Coordinate System

### D2291

Plane

### D2292

Axis

### D2293

Point

### D2294

Modeling Tab

### D2295

Sketch group:

### D2296

New Sketch (Large Button)

### D2297

Small Button Cluster

### D2298

Edit Sketch

### D2299

Attach Sketch

### D2300

Coordinate System (Small Button Dropdown)

### D2301

Coordinate System (Default)

### D2302

Plane

### D2303

Axis

### D2304

Point

### D2305

Modeling group:

### D2306

Extrude (Large Button)

### D2307

Revolve (Large Button)

### D2308

Medium Button Cluster

### D2309

Loft

### D2310

Helix

### D2311

Dress-Up group:

### D2312

Fillet and Chamfer (Large Button Dropdown)

### D2313

Fillet (Default)

### D2314

Chamfer

### D2315

Medium Button Cluster

### D2316

Draft

### D2317

Shell/Thickness

### D2318

Transformation group:

### D2319

Medium Button Cluster

### D2320

Mirror Feature

### D2321

Linear Pattern

### D2322

Medium Button Cluster

### D2323

Circular Pattern

### D2324

Multi Transform

### D2325

Primitives group:

### D2326

Primitives (Large Button Dropdown)

### D2327

Box (Default)

### D2328

Cylinder

### D2329

Sphere

### D2330

Cone

### D2331

Ellipsoid

### D2332

Torus

### D2333

Prism

### D2334

Wedge

### D2335

Tab (Disabled; not implemented)

### D2336

Other group:

### D2337

Medium Button Cluster

### D2338

Delete Face/Defeaturing

### D2339

Add Reference Object

### D2340

Surface Tab

### D2341

Surface group:

### D2342

Extend Face (Large Button)

### D2343

Small Button Cluster

### D2344

Filling

### D2345

Fill Boundary Curves

### D2346

Sections

### D2347

Small Button Cluster

### D2348

Curve on Mesh

### D2349

Blend Curve

### D2350

Sketch Tab

### D2351

Sketcher group:

### D2352

New Sketch (Large Button)

### D2353

Edit Sketch (Large Button)

### D2354

Small Button Cluster

### D2355

Attach Sketch

### D2356

Reorient Sketch

### D2357

Validate Sketch

### D2358

Small Button Cluster

### D2359

Merge Sketches

### D2360

Mirror Sketch

### D2361

Edit Mode group:

### D2362

Small Button Cluster

### D2363

Leave Sketch

### D2364

Align View to Sketch

### D2365

Toggle Section View

### D2366

Geometries group:

### D2367

Polyline (Large Button)

### D2368

Small Button Cluster

### D2369

Point

### D2370

Text (Experimental)

### D2371

Toggle Construction Geometry

### D2372

Small Button Cluster

### D2373

Line Tools (Small Button Dropdown)

### D2374

Polyline

### D2375

Line

### D2376

Line

### D2377

Arc Tools (Small Button Dropdown)

### D2378

Arc From Center

### D2379

Arc From 3 Points

### D2380

Elliptical Arc

### D2381

Hyperbolic Arc

### D2382

Parabolic Arc

### D2383

Small Button Cluster

### D2384

Circle and Conic Tools (Small Button Dropdown)

### D2385

Circle From Center

### D2386

Circle From 3 Points

### D2387

Ellipse From Center

### D2388

Ellipse From 3 Points

### D2389

Rectangle Tools (Small Button Dropdown)

### D2390

Rectangle

### D2391

Centered Rectangle

### D2392

Rounded Rectangle

### D2393

Regular Polygon Tools (Small Button Dropdown)

### D2394

Triangle

### D2395

Square

### D2396

Pentagon

### D2397

Hexagon

### D2398

Heptagon

### D2399

Octagon

### D2400

Polygon

### D2401

Small Button Cluster

### D2402

Slot Tools (Small Button Dropdown)

### D2403

Slot

### D2404

Arc Slot

### D2405

B-Spline Creation Tools (Small Button Dropdown)

### D2406

B-Spline

### D2407

Periodic B-Spline

### D2408

B-Spline From Knots

### D2409

Periodic B-Spline From Knots

### D2410

Constraints group:

### D2411

Dimension Tools (Large Button Dropdown)

### D2412

Dimension

### D2413

Horizontal Dimension

### D2414

Vertical Dimension

### D2415

Distance Dimension

### D2416

Radius/Diameter Dimension

### D2417

Radius Dimension

### D2418

Diameter Dimension

### D2419

Angle Dimension

### D2420

Lock Position

### D2421

Dimension (Large Button)

### D2422

Small Button Cluster

### D2423

Horizontal Dimension

### D2424

Vertical Dimension

### D2425

Distance Dimension

### D2426

Small Button Cluster

### D2427

Radius and Diameter Constraints (Small Button Dropdown)

### D2428

Constrain radius

### D2429

Constrain diameter

### D2430

Constrain auto radius/diameter

### D2431

Angle Dimension

### D2432

Lock Position

### D2433

Small Button Cluster

### D2434

Coincident / Point-on-object

### D2435

Coincident Constraint

### D2436

Point-on-object Constraint

### D2437

Small Button Cluster

### D2438

Horizontal and Vertical Constraints (Small Button Dropdown)

### D2439

Horizontal Constraint

### D2440

Vertical Constraint

### D2441

Horizontal Constraint

### D2442

Vertical Constraint

### D2443

Small Button Cluster

### D2444

Parallel Constraint

### D2445

Perpendicular Constraint

### D2446

Tangent/Collinear Constraint

### D2447

Small Button Cluster

### D2448

Equal Constraint

### D2449

Symmetric Constraint

### D2450

Block Constraint

### D2451

Small Button Cluster

### D2452

Group Constraint (Development preview)

### D2453

Constraint State (Small Button Dropdown)

### D2454

Toggle Driving/Reference Constraints

### D2455

Toggle Constraints

### D2456

Tools group:

### D2457

Small Button Cluster

### D2458

External Geometry (Small Button Dropdown)

### D2459

External Projection

### D2460

External Intersection

### D2461

Carbon Copy

### D2462

Move / Array Transform

### D2463

Small Button Cluster

### D2464

Rotate / Polar Transform

### D2465

Scale

### D2466

Offset

### D2467

Small Button Cluster

### D2468

Mirror

### D2469

Remove Axes Alignment

### D2470

Fillet and Chamfer Tools (Small Button Dropdown)

### D2471

Fillet

### D2472

Chamfer

### D2473

Small Button Cluster

### D2474

Curve Editing Tools (Small Button Dropdown)

### D2475

Trim Edge

### D2476

Split Edge

### D2477

Extend Edge

### D2478

B-Spline group:

### D2479

Small Button Cluster

### D2480

Geometry to B-Spline

### D2481

Increase B-Spline Degree

### D2482

Decrease B-Spline Degree

### D2483

Small Button Cluster

### D2484

Knot Multiplicity (Small Button Dropdown)

### D2485

Increase knot multiplicity

### D2486

Decrease knot multiplicity

### D2487

Insert Knot

### D2488

Join Curves

### D2489

Helpers group:

### D2490

Small Button Cluster

### D2491

Select Associated Constraints

### D2492

Select Associated Geometry

### D2493

Toggle Circular Helper for Arcs

### D2494

Small Button Cluster

### D2495

B-Spline Geometry Information (Small Button Dropdown)

### D2496

Toggle B-Spline Degree

### D2497

Toggle B-Spline Control Polygon

### D2498

Toggle B-Spline Curvature Comb

### D2499

Toggle B-Spline Knot Multiplicity

### D2500

Toggle B-Spline Control Point Weight

### D2501

Toggle Internal Geometry

### D2502

Switch Virtual Space

### D2503

Assembly Tab

### D2504

Assembly group:

### D2505

Create Assembly (Large Button)

### D2506

Insert Component (Large Button Dropdown)

### D2507

Insert Component

### D2508

Insert New Part

### D2509

Small Button Cluster

### D2510

Move Components

### D2511

Link Arrays (Small Button Dropdown)

### D2512

Circular Link Array

### D2513

Linear Link Array

### D2514

Path Link Array

### D2515

Point Link Array

### D2516

Polar Link Array

### D2517

Solve Assembly

### D2518

Small Button Cluster

### D2519

Exploded View

### D2520

Snapshot

### D2521

Simulation

### D2522

Small Button Cluster

### D2523

Bill of Materials

### D2524

Assembly Joints group:

### D2525

Small Button Cluster

### D2526

Toggle Grounded

### D2527

Create Rigid Group

### D2528

Fixed Joint

### D2529

Small Button Cluster

### D2530

Revolute Joint

### D2531

Cylindrical Joint

### D2532

Slider Joint

### D2533

Small Button Cluster

### D2534

Ball Joint

### D2535

Distance Joint

### D2536

Parallel Joint

### D2537

Small Button Cluster

### D2538

Perpendicular Joint

### D2539

Angle Joint

### D2540

Rack and Pinion Joint

### D2541

Small Button Cluster

### D2542

Screw Joint

### D2543

Gears Joint (Small Button Dropdown)

### D2544

Gears Joint

### D2545

Belt Join

### D2546

Mesh Tab

### D2547

Mesh Tools group:

### D2548

Import Mesh (Large Button)

### D2549

Small Button Cluster

### D2550

Export Mesh

### D2551

Mesh From Shape

### D2552

Regular Solid

### D2553

Mesh Modify group:

### D2554

Small Button Cluster

### D2555

Harmonize Normals

### D2556

Flip Normals

### D2557

Fill Holes

### D2558

Small Button Cluster

### D2559

Close Hole

### D2560

Add Triangle

### D2561

Remove Components

### D2562

Small Button Cluster

### D2563

Smooth

### D2564

Refinement

### D2565

Decimate

### D2566

Small Button Cluster

### D2567

Scale

### D2568

Mesh Boolean group:

### D2569

Small Button Cluster

### D2570

Union

### D2571

Intersection

### D2572

Difference

### D2573

Mesh Cutting group:

### D2574

Small Button Cluster

### D2575

Cut

### D2576

Trim

### D2577

Trim With Plane

### D2578

Small Button Cluster

### D2579

Section From Plane

### D2580

Cross-Sections

### D2581

Mesh Segmentation group:

### D2582

Small Button Cluster

### D2583

Merge

### D2584

Split by Components

### D2585

Segmentation

### D2586

Small Button Cluster

### D2587

Segmentation From Best-Fit Surfaces

### D2588

Mesh Analyze group:

### D2589

Small Button Cluster

### D2590

Evaluate and Repair

### D2591

Face Info

### D2592

Curvature Plot

### D2593

Small Button Cluster

### D2594

Curvature Info

### D2595

Evaluate Solid

### D2596

Bounding Box Info

### D2597

View Tab

### D2598

View group:

### D2599

Fit All (Large Button)

### D2600

Small Button Cluster

### D2601

Fit Selection

### D2602

Standard Views (Small Button Dropdown)

### D2603

Isometric

### D2604

Front

### D2605

Top

### D2606

Right

### D2607

Rear

### D2608

Bottom

### D2609

Left

### D2610

Align to Selection

### D2611

Small Button Cluster

### D2612

Draw Style (Small Button Dropdown)

### D2613

As Is

### D2614

Points

### D2615

Wireframe

### D2616

Hidden Line

### D2617

No Shading

### D2618

Shaded

### D2619

Flat Lines

### D2620

Measure

### D2621

Mass Properties

### D2622

Individual Views group:

### D2623

Small Button Cluster

### D2624

Isometric

### D2625

Front

### D2626

Top

### D2627

Small Button Cluster

### D2628

Right

### D2629

Rear

### D2630

Bottom

### D2631

Small Button Cluster

### D2632

Left

### D2633

Drafting Mode (Drawing)

### D2634

This mode is intended for creating blueprints. Its outline includes Home, Tools and View tabs. Specific command placement has not yet been specified; retain this section without inventing additional controls.

### D2635

CAM Mode

### D2636

CAM remains a selectable mode. No additional CAM toolbar or task-field changes are specified in this outline.

### D2637

Model Panel

### D2638

Keep the component definition, instance and history contracts consistent across the interface styles. The panel layouts below describe the specified presentation; the toolbar style selector must not change model ownership.

### D2639

Classic Model Panel

### D2640

Models: domestic definitions first, followed by nested imported-file groups and component instance counts.

### D2641

Part Tree: the file is the pinned top-level container, identified by its file name and FreeCAD icon. Linked component instances appear beneath it. The file container is not a component model in Models. Renaming the file row changes the file display name without renaming any component.

### D2642

In the Classic panel outline, history may be collapsed under each component instance. Editing a shared component definition affects all its instances.

### D2643

Do not show background Bodies as separately deletable objects.

### D2644

Attributes provides the former Model pane View and Data tabs.

### D2645

Plus Model Panel

### D2646

Models: first tab, domestic definitions first, then expandable imported-file groups. Include unused definitions and nested imported files, with component instance counts.

### D2647

A new document creates a domestic Part001 definition, places its first occurrence beneath the file, and enters Edit for that component. Part001 is ordinary: it can be renamed, removed or deleted. An empty file is valid. Existing documents gain the file container without adding another Part001 or changing component identities, geometry, placements or references. Opening an older .cadprt file adds this container in memory after checking the saved file. The original on disk stays unchanged until Save. The added file row stays pinned through Undo; reopening an upgraded file does not add another container. In Models, select one unused domestic definition and choose Delete component or press Delete. Remove its occurrences and outside references first; otherwise explain why deletion is blocked. Imported definitions must be opened in their defining file before deletion. Deleting the edited unused model restores the file view and closes its isolated component tab. Undo restores the definition and geometry without reopening that tab. Part Tree Delete removes occurrences only; the file row remains protected. Reference checks cover open files, not other closed assemblies on disk.

### D2648

Edit is the user-facing term for making a component active. Double-click or Edit in Models or Part Tree changes the active component and displays its History within the current file tab. Single-click only selects. Open in new window is available in both context menus and opens a component in a new file tab. Opening, closing or switching component tabs preserves the original tabâ€™s edited occurrence and camera view. A child component can also be edited in the separate tab, with the same contextual transparency behavior. In Part Tree, double-click the component name or icon to edit that exact occurrence, including a nested or repeated instance. Activation must work when the tree refreshes between clicks. A pending click must not change another tab or activate a removed occurrence. Finish an open modeling task before editing a different component.

### D2649

All occurrences of the active definition use bold name text and the configured active-item fill color in Models and Part Tree. The chosen occurrence retains a separate selection indicator. Models Edit reuses the last edited occurrence in the current tab, otherwise the first occurrence in Part Tree.

### D2650

Part Tree uses Part Type for Full Component, Bodies Only, Reference and Excluded. Visibility is a separate Shown or Hidden choice. Excluded geometry cannot be shown through visibility; change its Part Type first. The active component and its parent branch cannot be hidden. Editing an excluded component restores its own editing display without changing the exclusion saved by its parent.

### D2651

Part Type choices are saved on the active component for itself and its direct children, shared by every instance of that component and retained through save/reopen. The active component defaults to Full Component; its children default to Bodies Only. The active component may use Full Component or Bodies Only. Reset to Default restores the applicable default. Edit a deeper component's owner before changing that child's type. Switching the active component restores its saved choices.

### D2652

A direct Reference child shows its full component geometry while its owner is edited, respecting nested exclusions. When editing an ancestor, that Reference behaves as Excluded; returning to its owner restores Reference. To reference geometry from an excluded nested child, add that child separately as a direct Reference. Source Reference geometry contributes no final geometry and cannot be used directly for modeling: Add Reference Feature is required to create an owned, derived and linked reference body, sketch or other supported feature. Existing owned reference features remain part of the edited component.

### D2653

Existing nested display overrides remain effective until the affected child receives an explicit Part Type. New Part Type choices take precedence without changing another component's saved data. Parent and sibling geometry remains at least 75% transparent while the edited component and its descendants retain authored appearance.

### D2654

Geometry outside the chosen active occurrence and all its descendants is at least 75% transparent, preserving any greater existing transparency. Other occurrences of the same definition are also faded. Restore normal appearance when the edit context changes; authored visibility and transparency are preserved. Preserve component and individual face colors. Apply the transparency floor separately to each material, retaining faces already more transparent than 75%. This display belongs to the current file tab and does not change saved appearance settings.

### D2655

Editing the file row shows only its fixed Origin and origin planes in History, with visibility controls. These establish global coordinates and support placement and assembly alignment. Geometry creation and editing require explicitly activating a component. Every component retains its own origin. When the file is active, all components use their normal transparency. File Edit refreshes references within its domestic component assembly without creating file-owned geometry or History entries. The Datum Plane action is disabled while the file is being edited; selecting a component alone does not enable it. Sketch and datum-plane commands must refuse the file as their destination before opening a task or changing the document. Move Components can change occurrence placements beneath the file, with Undo and Redo, without adding modeling History to the file. In a component document, the Part workbench Primitive, Extrude, Revolve, Loft and Sweep commands use the shared component tasks; Sweep opens Pipe. They require an edited component and must not fall back to a legacy dialog when file Edit refuses modeling. Legacy documents retain their existing Part dialogs. Native Part Boolean, copy, shape, datum, direct primitive and link-array commands are disabled during file Edit. Selecting geometry does not enable them. Direct invocation must leave objects, visibility and undo history unchanged. Inspection and display controls remain available.

### D2656

Importing external files adds their models to Models only; an entire external file cannot be inserted as a Part Tree occurrence. Changes to the Add Component workflow are deferred.

### D2657

Editing an unused model temporarily displays it as the last Part Tree item, labelled Component name (unused model), retaining external-file qualification. Apply active fill and bold text. The temporary item supports editing but cannot be reordered or treated as a permanent assembly occurrence. Unused models otherwise remain in Models only; they do not appear as additional permanent Part Tree roots. Child components remain available for editing within the temporary view.

### D2658

While editing an unused model, gray all existing Part Tree entries and force their geometry hidden. Those entries remain selectable and available for Edit; visibility controls cannot override this hiding. Editing another component or the file removes the temporary item and restores prior visibility. Saving retains component edits but excludes the temporary entry and temporary hiding state. The temporary view does not change the assembly visibility settings saved with the file.

### D2659

Part Tree: linked component instances support Cut/Paste and drag/drop rearrangement beneath the pinned file container. File-level assembly relationships and placement controls are managed here without file-owned modeling geometry. With the file in Edit, right-click one top-level occurrence to Ground component at its current position or Unground component. Grounding applies to that occurrence, including occurrences of external models, and does not change the shared definition. Expand grouped instances to choose one occurrence. Nested or multiple selections, component Edit, unused-model Edit and unfinished tasks cannot change file grounding. Selecting the file once does not enter Edit. Grounding and ungrounding support Undo/Redo and keep the current tab and origin-only Model History. Changing Edit context while a menu is open cancels that action.

### D2660

Fixed relationships: while the file is in Edit, select two individual top-level occurrences and choose Fix relative position. Their current positions and orientations are retained; at least one must already be grounded or connected to a ground. Right-click the file or an occurrence and choose Assembly relationships to review Ground and Fixed relationships. Entries identify components by qualified name and occurrence number. Selecting entries highlights their components without changing Edit context or Model History. Edit fixed offset changes the second component relative to the first using X, Y and Z in millimeters and yaw, pitch and roll in degrees. Cancel or accepting unchanged values makes no change. Remove selected removes relationships, keeping the components; removing a ground releases its placement lock. Applied changes support Undo/Redo. Changing Edit context or deleting a listed relationship prevents a stale dialog from applying changes. These controls keep the current file tab and origin-only file History.

### D2661

History: sequential operations for the active component.

### D2662

Origin is first, visible by default and protected from deletion.

### D2663

Origin Planes is its own child, hidden by default and protected from deletion.

### D2664

Hide core Body objects and retain their feature ownership in the background.

### D2665

On first startup, Components is visible at the top left and occupies about two-thirds of the left panel height. Attributes is below it and occupies about one-third. Tasks is docked on the right and shows New File and Open with no document. Subsequent startups restore the user-customized positions, floating state and sizing of panels and toolbars instead of resetting this initial layout.

### D2666

Attributes retains functional View and Data tabs.

### D2667

Toolbar Operations/Feature & their Task Panel Workflows

### D2668

Combine the specified additive and subtractive Part Design operations into shared feature workflows. Preserve their native parameters and the additional fields specified here. A change in icon, toolbar grouping or task layout must not silently remove a required field or choice.

### D2669

Use the same task pane for creating and editing a feature.

### D2670

Section 1: Main Parameters, expanded by default.

### D2671

Boolean choice: New Body, Add or Subtract. Show the target Body selector for Add and Subtract only; the selected target remains a background result object.

### D2672

Profile selection: Whole Sketch or Selected Curves, with a list of the selected curves.

### D2673

Keep Mode and Type as separate fields: Mode controls sidedness; Type controls the extent or termination.

### D2674

Section 2: Dimensions, expanded by default.

### D2675

Retain the applicable direction selector, sketch-normal default, length and reverse-direction arrow buttons.

### D2676

Retain Offset and the other dimensions native to the selected operation, including taper or angular fields where applicable.

### D2677

Section 3: Advanced/Optional, collapsed by default. Keep applicable native controls available rather than deleting them to simplify the main section.

### D2678

Section 4: Preview, expanded by default.

### D2679

Retain Recompute on Change and the preview choices None, Overlay and Result. Overlay is the default.

### D2680

Overlay colors: blue for New Body, green for Add and red for Subtract. Show the full tool even without a target or Boolean intersection.

### D2681

Keep preview behavior consistent when fields, profile selection, direction or termination change.

### D2682

General

### D2683

General but No Workflows Needed

### D2684

The common toolbar retains New File, Open, Save, Save As, Undo, Redo, Recompute, Cut, Copy and Paste. New File uses the native New Document icon. Detailed command placement and the complete button descriptions remain in TOOLBARS.md.

### D2685

Structure

### D2686

Use the component definition/instance distinction for structure actions. Do not create both a visible definition and a linked occurrence as two assembly instances when the user requests one.

### D2687

New Part

### D2688

Use component definitions for both parts and assemblies.

### D2689

New Component offers domestic storage in the active componentâ€™s defining file, a new external file, or an existing external file. Choose a location for a new file or select the existing file, then enter a unique component name. Creation does not place an instance in the current assembly. A new external file contains the named component beneath its pinned file row, without an extra Part001. Add Component places one linked instance under the active component.

### D2690

If the active component definition is shared, its child structure is shared by all its instances.

### D2691

Name automatically added parts Part001, Part002, Part003 and so on, using the next available number.

### D2692

Deleting an instance from Part Tree leaves its definition available in Models.

### D2693

Domestic components belong to the current file. External components belong to imported files. Display a domestic name as M3 screw and an external name as M3 screw (Hardware). The qualifier is the source filename; use its path when identical filenames would be ambiguous. Names must be unique within a file, but different files may contain components with the same name.

### D2694

Import Component File adds a collapsible file group to Models without placing a component. Show all components in that file, including unused components, and nested file imports beneath its definitions. Removing the last placed instance retains the imported file in Models. A missing file remains visible with Locate Component File for recovery.

### D2695

Activating an external component edits its defining file. New components and file imports use that defining file. A subcomponent must be domestic to that file or available through a file imported directly there. For example, activate M3 screw (Hardware), import Coatings into Hardware, then add a Coatings component beneath M3 screw. Block circular file imports and circular component nesting immediately.

### D2696

Edits to an external component save to its defining file. Other assemblies using that file receive the saved change when they reopen. Display the external file qualifier in the editing indication so the destination of shared edits is clear.

### D2697

Copy to Domestic Components creates a separate definition and copies its domestic subcomponent hierarchy. Existing external child definitions remain shared. Prompt with a checklist of placements in the domestic file to replace; leave all unchecked by default. Cancel keeps the new copy and leaves placements unchanged. Preserve placement positions when replacing. Explain any downstream reference or display override that must be repaired before replacement.

### D2698

Copy to External File creates an independent file definition and retains the original definition and its placements. Do not offer an identity-preserving move between domestic and external storage. Editing a copied definition does not change the original definition. The destination file places the copied component beneath its pinned file row, without creating an extra Part001.

### D2699

Coordinate System

### D2700

Provide a Coordinate System action in the new-file Tasks pane and as a medium Home action.

### D2701

Its dropdown offers Plane, Axis and Point.

### D2702

Datum Plane

### D2703

Make Datum Plane available from the new-file Tasks pane and within New Sketch creation.

### D2704

Section 1: Plane orientation and location. Select geometry is the default; Enter values is the alternative. The shared selection list accepts an origin/user plane, flat face, two coplanar non-collinear body edges or lines (including an origin axis with a line), three non-collinear points, or a line and an off-line point. Planar curves may participate; reject contradictory or non-coplanar geometry. An adjacent [...] menu offers XY, YZ and XZ planes. Show Under-defined, Defined or Invalid with an explanation. Enter values exposes X/Y/Z offsets and x'/y'/z' normal components, normalized on acceptance. Provide Reverse normal direction and a signed Offset distance with its own Reverse button.

### D2705

Section 2: Orientation. Use the same shared selection list for the projected X direction. Accept one body edge, line or origin axis, or two points including curve endpoints. The adjacent [...] menu offers X, Y and Z axes. Show Under-defined, Defined or Invalid. An empty list defaults to the component axis closest to the plane; break ties X, then Y, then Z. Project the chosen direction onto the plane; reject a zero projection. Provide Reverse direction for +X versus -X; derive Y to keep a right-handed frame.

### D2706

Section 3: Origin selection. A single-item selection textbox defaults to the part origin projected onto the plane. Clicking the field activates picking of an origin, point or curve endpoint. Project the selected point onto the plane. Delete clears the reference and restores the default.

### D2707

Section 4: Preview. Preview enables a translucent purple plane overlay; Recompute on update controls automatic updates. Both checkboxes default on. The overlay creates no document object and cannot intercept selections. When automatic updates are off, toggling Preview off/on refreshes it; OK always validates and recomputes the saved plane.

### D2708

A plane created while preparing a sketch becomes an available sketch attachment in the same workflow.

### D2709

Datum Line

### D2710

Keep Axis available from the Coordinate System dropdown. No additional task-field changes have been specified.

### D2711

Datum Point

### D2712

Keep Point available from the Coordinate System dropdown. No additional task-field changes have been specified.

### D2713

New Group

### D2714

No additional New Group changes are specified.

### D2715

Make Link

### D2716

Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

### D2717

Make Sub-Link

### D2718

Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

### D2719

Replace with Link

### D2720

Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

### D2721

Unlink

### D2722

Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

### D2723

Import Links

### D2724

Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

### D2725

Import All Links

### D2726

Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

### D2727

Variable Set

### D2728

No additional Variable Set changes are specified.

### D2729

Part Design Workbench

### D2730

Helper Features Group

### D2731

New Sketch

### D2732

Open a sketch creation task without requiring a Body or attachment to another object.

### D2733

Show the origin XY, XZ and YZ planes when New Sketch is clicked. Clicking a plane selects and highlights only that plane and updates the task selector. Keep the other planes visible without selecting the whole Origin container. Retain temporary visibility restoration on Cancel and Base layer hiding of individual datums.

### D2734

Choose an origin plane, an existing user-created plane, one planar body face, two coplanar edges of one body, or Independent plane. Independent plane defines the sketch origin X, Y and Z and its orientation with rotation angles or explicit in-plane and normal directions, in component coordinates. Creating a separate datum plane remains available.

### D2735

Retain the plane selector and Offset field. Follow support is enabled by default; turn it off to copy the selected frame once without an attachment. Independent plane has no support. Reject collinear or non-coplanar edge pairs that do not define one flat plane.

### D2736

On OK, close the creation task before opening Sketcher. Do not show the prompt that another task dialog is already open.

### D2737

Retain New Sketch, Attach Sketch and Edit Sketch actions. For a body face, two-edge or user-plane attachment, save the last valid support plane location and orientation and the sketch origin and axes. Follow valid support movement. If the support is deleted, missing or unavailable because of an upstream error, keep the sketch at exactly its last valid frame and allow editing and downstream modeling. Resume following when the same support is repaired or restored by Undo; never attach to an unrelated replacement with the same name. Preserve the frame and support references through save/reopen.

### D2738

In Sketcher, retain active and reference curves, active and reference dimensions, and geometric constraints.

### D2739

Use Sketch001 for the first sketch in each component, independently of sketches in other components.

### D2740

Modeling Features Group

### D2741

The following sections capture the specified shared modeling workflows and the fields that must remain available.

### D2742

Extrude

### D2743

Combine Classic Pad and Pocket into Extrude, using the Pad icon. Classic Pad opens Add; Classic Pocket opens Subtract.

### D2744

Section 1: Main Parameters.

### D2745

Boolean: New Body, Add or Subtract; target Body selector for Add and Subtract only.

### D2746

Profile choice: Whole Sketch or Selected Curves. List all chosen curves in the task pane and allow a subset of a sketch.

### D2747

Selected curves must belong to the same sketch and form closed, non-self-intersecting boundaries.

### D2748

Require one connected region, with optional holes. Separate disconnected regions are not accepted as one extrusion.

### D2749

Clicking the area between two sets of closed curves in the viewport adds both boundary sets to the selected-curves list.

### D2750

Mode: One Sided, Two Sided and Symmetric. Preserve the familiar one-dimension, two-dimension and symmetric choices.

### D2751

Type: Dimension, To Last, To First, Up to Face/Surface and Up to Shape, with the native termination choices applicable to the operation retained.

### D2752

Section 2: Dimensions.

### D2753

Direction defaults to Sketch Normal; retain direction selection and reverse arrow buttons.

### D2754

Retain Length, the second length for Two Sided mode, Taper Angle and Offset, with the applicable termination reference fields.

### D2755

Section 3: Advanced/Optional. Keep applicable native Extrude settings available.

### D2756

Section 4: Preview.

### D2757

Retain Recompute on Change and None, Overlay and Result; default to Overlay.

### D2758

Show blue New Body, green Add and red Subtract preview volumes.

### D2759

Document window interaction.

### D2760

Show the selected preview and allow the specified handles to change Length and Taper Angle.

### D2761

Keep the background Body attached to its parent Extrude. Do not permit independent pane deletion to leave a visible orphaned solid.

### D2762

Revolve

### D2763

Combine Revolve and Groove into a shared additive/subtractive revolve workflow.

### D2764

Use the common task sections, preserving the native axis, angular extent, direction, target and termination fields applicable to the operation.

### D2765

Keep the colored Add/Subtract preview and the applicable native fields when changing the toolbar presentation. Additional angular-field changes are not specified here.

### D2766

Loft

### D2767

Combine Additive Loft and Subtractive Loft into the shared Loft workflow.

### D2768

Preserve the native section selection and applicable Loft fields, together with the common Boolean, target and preview controls.

### D2769

Helix

### D2770

Combine Additive Helix and Subtractive Helix into the shared Helix workflow.

### D2771

Preserve the native Helix geometry and dimension fields and the common Boolean, target and preview controls.

### D2772

Primitive

### D2773

Combine additive and subtractive primitives into the shared Primitive workflow.

### D2774

Preserve the selected primitive type and its native dimensions, with the common Boolean, target and preview controls.

### D2775

Dress Up Features Group

### D2776

Keep Fillet/Chamfer, Draft, Shell/Thickness and Delete Face/Defeaturing available in the Modeling Dress-Up group. No additional field changes are specified for these features.

### D2777

Transformation Features Group

### D2778

Keep Part Design transformation operations in the Modeling Transformation group.

### D2779

Pattern editing must show individual instance suppression controls immediately on opening. Suppress or restore a selected copy without losing direction, reference collectors or the shared Linear/Circular settings; accepting with live preview disabled must still apply the final parameters. MultiTransform supports Circular, Path and Point Pattern entries and opens the matching native parameter editor. Preserve the Plus unified Pattern entry and its existing ribbon groups.

### D2780

Part Workbench

### D2781

No additional feature workflow changes are specified for this workbench in this outline.

### D2782

Surface Workbench

### D2783

No additional feature workflow changes are specified for this workbench in this outline.

### D2784

Assembly Workbench

### D2785

No additional feature workflow changes are specified for this workbench in this outline.

### D2786

Draft Workbench

### D2787

No additional feature workflow changes are specified for this workbench in this outline.

### D2788

Mesh Workbench

### D2789

No additional feature workflow changes are specified for this workbench in this outline.

### D2790

CAM Workbench

### D2791

Preserve the existing CAM workflows while applying the inherited controls and behavior below.

### D2792

CAM operations and dress-ups use the selected work plane origin and orientation consistently in preview, inspection and post-processing. Avoid Faces keeps the selected regions protected with the corrected Safe STL clearance. Missing or invalid inputs must clear the generated toolpath and report the failure, including failed holding-tag generation and probe-map points outside the valid area. The CAM Job preferences include the Sanity report output-file setting; Mill Facing offers Circular clearing, and Simple Copy opens its native task.

### D2793

Workflows

### D2794

Application startup

### D2795

Show native recent-file cards in the viewing window at startup, without New File option cards or example files. An empty list shows No recent files. New File and Open remain visible in Tasks. Prepare the selected theme, toolbar style and restored workspace before exposing the main window; do not cycle through workbenches after it appears. Home loads only its required native command modules. Explicit theme and Plus/Classic choices persist.

### D2796

The Tasks pane offers New File and Open before a file exists.

### D2797

Show Components above Attributes at the left with approximately a two-thirds/one-third height split.

### D2798

After New File

### D2799

The Tasks pane offers New Sketch, Coordinate System, Datum Plane and Add Component.

### D2800

Create the first automatic part as Part001 and use untitled001 for the default file name.

### D2801

Status controls

### D2802

Keep the notification/status control, navigation-style selector and units selector present and functional.

### D2803

Build handoff

### D2804

Every new owner build must update FreeCADPlus.exe - Shortcut to the intended executable. Verify the shortcut target and working directory before presenting the build for testing. Store all validation output only in C:\Users\GAMING-PC\Documents\_temp\freecad\validation; delete task output after recording its verified results in the canonical documentation. Store useful test payloads, native build trees and required build dependencies only in C:\Users\GAMING-PC\Documents\_temp\freecad\test-builds. Remove obsolete builds after verifying the retained build and retargeted shortcut. Preserve source, owner documents, preferences and original workload archives. October 6 relocation retains the current palette payload and native build; it changes no UI, geometry or acceptance claims.

### D2805

Defaults

### D2806

Toolbar interface: Plus UI.

### D2807

Navigation style: Blender.

### D2808

Units: Imperial Decimal.

### D2809

Default document name: untitled001.

### D2810

First automatically added part: Part001, then the next available number.

### D2811

First sketch in each component: Sketch001; first background Body: Body001.

### D2812

Origin visible for the active component; Origin Planes hidden.

### D2813

Preview: Overlay, using blue for New Body, green for Add and red for Subtract.

### D2814

Apply defaults to unset preferences; keep the selectors functional so the user can change and retain their choices.

### D2815

Owner screenshot defaults approved October 2 2026

### D2816

General: English; Imperial Decimal (in, lb); 3 decimal places. Honor project units. Use operating-system number formatting; do not substitute the decimal separator.

### D2817

Application: FreeCAD Light theme; medium 24 px toolbar icons; Combined Tree View and Property View; 4 recent files. Tiled background off; cursor blinking and startup splash on. Panels start docked, with Tasks on the right. Migrate the old implicit Tasks overlay once; retain other overlay memberships and subsequent user customization. Retain Plus UI and Blender navigation defaults.

### D2818

Selection

### D2819

Preselection on, yellow #FFFF00; selection on, amber #FFBF00; pick radius 5 px. Tree hover preselection, automatic view switching, automatic tree expansion, selection history and tree selection checkboxes off.

### D2820

Display colors

### D2821

Simple background #F7F7F7; linear and radial gradients off. Object being edited #00AAFF; active container #5BB413. Color bar label #212529, 13 pt.

### D2822

Sketcher appearance

### D2823

Creating line, coordinate text and cursor crosshair: #212529.

### D2824

Geometry: constrained #005500; unconstrained #00AA00; solid lines, 2 px.

### D2825

Construction and internal alignment geometry: constrained #5555FF; unconstrained #00AAFF; dashed lines (6:2), 2 px.

### D2826

External construction geometry: #FF00FF; short dashed lines (3:1), 2 px. External defining geometry: #CC3399; solid lines, 2 px.

### D2827

Fully constrained sketch: #000000. Invalid sketch: #FF0000.

### D2828

Constraint symbols and dimensional constraints: #0000FF. Reference constraints: #00AAFF. Expression-dependent constraints: #FF00FF. Deactivated constraints: #868E96.

### D2829

Outside Sketcher: vertices and edges #000000; face swatch #CBDFF4.

### D2830

Document maintenance

### D2831

Every owner-requested change must update ai-instructions/ui/FreeCAD Plus UI & UX.docx. Preserve this Word document, its heading structure, native automatic numbering and owner edits. Capture changed requirements and behavior that must remain available; record validation separately from specification.

### D2832

Apply these defaults to unset preferences in new profiles; preserve subsequent saved user choices. The owner explicitly requested applying this preset to the closed development build profile as well.

### D2833

Sketch drawing validation, October 2: Plus New File, New Sketch and curve creation pass native Qt input checks for line, circle, arc and rectangle, including save/reopen. The reported pointer-input failure remains unconfirmed and is not marked fixed; desktop capture prevented physical pointer acceptance.

### D2834

October 2 batched build: all completed source changes are incorporated, including the exact Design Home, Modeling, Sketch, Assembly and View ribbons, master-first component trees, unused assemblies and screenshot defaults. Packaged acceptance has 57 passing checks, including curve creation and save/reopen plus three launcher cold restarts, without source overlays. Compatible Python updates reuse the verified native engine. The reported physical sketch drawing failure remains unresolved. Related changes are grouped into validated commits and pushed to origin at completed milestones. Each delivered build must pass the desktop shortcut target and working-directory verification gate.

### D2835

Datum-plane create/edit uses the four sections specified above from the standalone Plus Plane action, native Datum Plane command in a component document, and component History editing. Both geometry lists reuse the modeling curve collector with broader reference filters, latest-item highlighting, repeat-click deselection, Remove/Clear and Delete. Plane inputs accept faces, planes, axes, edges, curves and points; orientation accepts edges, axes and points. Retain associative native dependencies, Undo/Redo, save/reopen, public PartDesign plane identity and hidden-helper cleanup. Opening older planes preserves their frame; legacy arbitrary rotations are retained as explicit values with stored origin and X direction. Existing sketch attachment and embedded Create Datum Plane behavior remain available. All task forms inherit Qt and active-theme colors. Prohibit task-level stylesheets that force foreground/background palette colors across child widgets, and copied form palettes that freeze colors. Preserve native dropdown, disabled-text and live theme handling; ribbon colors refresh with palette changes. Keep origin axes and planes small normally; show axes, planes and the origin point at twice normal size during plane and sketch placement editors, then restore prior size and visibility. Use a narrow task panel with vertical scrolling only. WORK_STATE records native build, runtime checks, document review and owner shortcut delivery separately; physical owner acceptance remains separate.

### D2836

Unified Revolve: Plus combines additive Revolution and subtractive Groove in one Tasks workflow for both creation and history editing. Main parameters, Dimensions, Advanced and Preview are collapsible sections. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, a target body shown only for Add or Subtract, a whole-sketch or selected-curves list, One angle / Two angles / Symmetric mode and native applicable extent types.

### D2837

Dimensions retains sketch vertical or horizontal axes and picked local axis references, angle values with synchronized direction arrows, and signed angular offsets from -360 through +360 degrees with an offset-flip arrow. Symmetric disables direction reversal. Entering a nonzero offset selects Offset automatically. Reference starts, first/last or surface termination, axis projection and refinement remain available where applicable. The rotational axis replaces the extrusion-only sketch-normal direction and angle replaces linear length.

### D2838

Preview offers Recompute on change, enabled by default, and None, Overlay or Result; Overlay is the default and uses blue for New Body, green for Add and red for Subtract. Cancel restores visibility and removes preview geometry. Native Revolution and Groove features retain geometry semantics. Type-changing edits preserve the component operation identity and published result references through undo/redo and save/reopen. Expression-driven definitions remain protected from task overwrites and can be edited through their native properties. Runtime acceptance and owner-build delivery are recorded separately in the roadmap and WORK_STATE.

### D2839

Unified Loft: Plus combines Additive Loft and Subtractive Loft in one component Tasks workflow for creation and History editing. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters has New Body, Add or Subtract, a target shown only for Add or Subtract, ordered sections, and Smooth or Ruled interpolation. Sections accept whole profiles, selected closed sketch regions with optional holes, or native end vertices. Retain ordered preselection and empty startup. Provide append, replace, remove, clear and section inspection.

### D2840

Loft Dimensions provides Move up, Move down and Reverse order. Section placements define the span; extrusion lengths, angular extents and offsets do not apply. Advanced retains Closed, Refine and Fuzzy tolerance: zero uses the native default; negative values request automatic tolerance. Preview has Recompute on change enabled and None, Overlay or Result. Default Overlay is blue for New Body, green for Add and red for Subtract. Cancel removes previews and restores visibility. Retain native geometry, associative sections and component result identities through edits, Boolean mode changes, undo/redo and save/reopen. Reject invalid or ineffective Booleans and protect expression-driven definitions from task overwrites.

### D2841

Loft validation, October 3: eight Loft and four Revolve/ribbon checks pass on an isolated fork candidate without source overlays. Task rendering was inspected. Native command routing, batched owner delivery and physical acceptance remain pending; roadmap and WORK_STATE hold evidence. The earlier sketch-drawing report remains unresolved.

### D2842

Unified Pipe: Plus combines Additive Pipe and Subtractive Pipe in one component Tasks workflow for creation and History editing, with one Pipe button after Loft in Modeling. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, a target only for Add or Subtract, ordered whole-profile or selected closed sketch-curve sections, append/replace/remove/clear, Constant or Multisection mode, and Transformed/Right corner/Round corner transition type. Constant retains additional sections for later Multisection use. Allow empty startup and ordered profile/path/section preselection.

### D2843

Pipe Dimensions collects the sweep path as a whole curve object or selected edges from one local object, with pick/remove/clear controls and section reordering. Path geometry and section placements define length and direction; extrusion lengths and offsets do not apply. Advanced retains Standard/Fixed/Frenet/Auxiliary/Binormal orientation, a separate auxiliary-path collector, curvilinear equivalence, binormal XYZ, native Subtraction/Common, Refine and Fuzzy tolerance. Preserve inactive options and stored tangent flags; native tangent expansion and Linear/S-shape/Interpolation scaling laws are not implemented. The inherited Pipe engine requires closed sections and cannot accept point-ended sections; report this clearly. Preserve native orientation and corner semantics.

### D2844

Pipe Preview retains Recompute on change enabled, None/Overlay/Result, and default Overlay colors blue/green/red for New Body/Add/Subtract. Cancel restores visibility. Preserve native associative profile/path links, component operation and result identities, downstream references, undo/redo and save/reopen through edits and Boolean type changes. Reject invalid, stale or cyclic inputs and ineffective Booleans atomically; protect expressions. October 3 validation: seven Pipe cases, eight Loft regressions and two ribbon checks pass in an isolated candidate without overlays; task captures were reviewed. Native command routing and grouped owner-build/shortcut delivery remain pending, as do physical pointer/high-DPI checks. Roadmap and WORK_STATE hold evidence.

### D2845

Unified Helix: Plus combines Additive Helix and Subtractive Helix in one Tasks workflow for creation and History editing, with one Helix ribbon button and no additive/subtractive dropdown. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, an explicit target only for Add or Subtract, whole-profile or selected closed sketch-curve collection, and the four native modes Pitch-Height-Angle, Pitch-Turns-Angle, Height-Turns-Angle and Height-Turns-Growth. Helix has no independent sidedness or extent Type. Retain empty startup, preselection and curve add/remove/clear controls.

### D2846

Helix Dimensions retains sketch vertical (default), horizontal, normal and construction axes, direct component X/Y/Z choices, and picked or typed datum/origin/straight-edge/circular-edge axes. Show the selected mode's pitch, height, turns, cone angle or radial growth fields; derive dependent values when changing modes. Preserve the separate axial reverse arrow and Left handed choice. Suggest pitch and height from the profile uses the native bounds heuristic, also applied to initial preselection. Without a profile, defaults are pitch 10 mm, height 30 mm, 3 turns and zero angle/growth. Height-Turns-Growth supports native flat spirals. Advanced retains Subtraction/Common, Refine, fusion tolerance factor (default 0.1) and Fuzzy tolerance; the fusion factor is not a length. Do not invent extrusion-only length offsets or termination choices.

### D2847

Helix Preview retains Recompute on change enabled and None/Overlay/Result, default Overlay with blue/green/red for New Body/Add/Subtract. Cancel restores visibility. Preserve native geometry, associative references, component operation and published result identities, downstream consumers, undo/redo and save/reopen. Invalid geometry, stale/cyclic inputs and ineffective Booleans cannot be accepted; failed edits roll back and expressions remain protected. October 3: eight Helix cases and ten shared Loft/Pipe/Revolve/ribbon regressions pass in an isolated candidate without overlays; normal and expanded task captures were inspected. Native command routing, grouped owner-build/shortcut delivery and physical pointer/high-DPI checks remain pending. Native Refine fallback warnings are retained in the evidence; valid geometry does not certify successful splitter removal. See roadmap and WORK_STATE.

### D2848

Unified Primitive: Plus combines Additive and Subtractive Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism and Wedge into one creation and History editing task. Modeling retains one Primitive action and the Primitives dropdown presets a shape in the same task. Classic documents retain native Body tasks. Tab remains disabled because no native Tab feature exists. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters contains New Body, Add or Subtract, an explicit target only for Add or Subtract, and the shape selector. No sketch profile is required.

### D2849

Primitive Dimensions preserves every native shape property and default, including cylinder/prism X and Y skew, prism sides, angular limits and all ten wedge bounds. Shape switches retain the drafts dimensions during the task. Advanced retains the native attachment modes, ordered references with Add selected, Remove and Clear, reversal, path parameter and offset. Unattached primitives expose component-local XYZ and yaw/pitch/roll; attached primitives expose their offset. Defaults are Box, unattached, zero placement, Refine enabled and fuzzy tolerance zero. Subtract retains Subtraction or Common. Native attachment and dimension properties remain associative and editable.

### D2850

Primitive Preview uses Recompute on change enabled and None, Overlay or Result, default Overlay, with blue/green/red for New Body/Add/Subtract. Cancel restores display state. Shape or mode changes preserve operation and published-result identity, downstream consumers and History order. Native geometry, attachments, undo/redo and save/reopen remain intact; invalid solids, ineffective Booleans, stale/cyclic inputs and expressions are guarded. October 3 grouped PartDesignGui build passes, with all 26 Loft/Pipe/Helix acceptance cases including routing, seven Primitive acceptance cases and eight inherited primitive regressions. Native ellipsoid Boolean results match directly configured Classic features; independent Part Boolean integration can differ. The dynamic Wedge layout was corrected after visual review. Owner delivery and final task captures are recorded in WORK_STATE; physical pointer/high-DPI checks and the earlier sketch drawing report remain pending. Native Refine and startup warnings remain in the evidence.

### D2851

October 3 fresh owner build: all enabled Release targets were built and staged in a new portable folder. Existing workflows and defaults are retained. All 22 staged modeling/startup checks passed without source overlays. The desktop shortcut target and working directory were updated and verified. WORK_STATE records build identity, paths and evidence. Physical pointer/high-DPI and earlier sketch drawing acceptance remain pending.

### D2852

October 3 ribbon and sketch feedback: the ribbon background must match surrounding panels in the active theme. Leaving sketch edit displays unfilled curves. During component Extrude region collection, closed sketch areas use translucent light blue, distinct from solid shading. An interior click can choose a sketch without first selecting it in the Profile field and collects all boundary curves, including holes, in Selected curves. Turning region picking off or closing the task removes its temporary fill. Retain individual edge selection, green/red volume previews and the shared profile collectors in Revolve, Loft, Pipe and Helix.

### D2853

Deleting an Extrude must preserve its source sketch, remove unused internal profile helpers and make the sketch available again when no other operation consumes it. Both edge and region selection must support creating another Extrude. Delete, Undo and Redo retain geometry and visibility consistently; shared inputs remain protected. Build, automated regression, visual inspection and owner acceptance are recorded separately in WORK_STATE.

### D2854

Compact Tasks panels: component Extrude, Revolve, Loft, Pipe, Helix, Primitive and Sketch/Datum Plane forms must remain usable in a narrow panel. Use vertical scrolling when the controls exceed the available height; do not require horizontal scrolling. Labels wrap above fields when space is limited. Long object names and attachment descriptions must not force the panel wider; dropdowns and curve lists retain full text in tooltips. Arrange vector components vertically, group collection buttons in short rows, and retain usable reference entry fields with Pick/Clear below them. Preserve all field values, native units, section defaults and create/edit/preview behavior.

### D2855

Narrow-panel acceptance covers a 360 logical-pixel Tasks dock with all applicable sections expanded, two-sided Extrude and custom direction, Primitive Wedge dimensions and attachment, and Sketch axis directions. Every displayed field must remain horizontally within the viewport and reachable by vertical scrolling. Retain the native task scroller and OK/Cancel controls. Build identity, automated checks, inspected captures, desktop shortcut delivery and physical owner acceptance are recorded separately in WORK_STATE.

### D2856

Build folder naming: all new builds use freecad_plus_[yyyy-mm-dd]_[test_case], for example freecad_plus_2026-10-03_extrude_frame. Use the build date and a descriptive test-case name separated by underscores. Apply this convention to new compilation folders and owner build output folders under a parent directory outside Google Drive. Preserve build identity, validation evidence and the existing desktop shortcut delivery checks. This records the naming rule without renaming existing builds or changing application behavior.

### D2857

Sketcher grid default: new sketches start with the grid hidden when no explicit grid preference is saved. Seed the native Mod/Sketcher/General ShowGrid preference to false. Keep the Sketcher grid toggle and preferences available so the user can enable it. Preserve explicit saved preferences and each existing sketch's stored grid visibility; do not reset the grid each time sketch edit opens. This preference-only change retains geometry, units and grid spacing. Runtime checks, the owner build and shortcut delivery are recorded in WORK_STATE.

### D2858

Curve-selection feedback: throughout component Extrude, Revolve, Helix, Loft and Pipe tasks, collected curves stay highlighted in the selection color, including while editing an existing operation, changing fields or showing a solid preview. After the first curve is collected, other sketches show light-medium gray curves and no area shading. Keep light-blue region shading only on the active sketch when region picking is enabled. Loft retains highlights for all collected sections; Pipe includes its profile, sweep path and active auxiliary path. Changing collectors updates the emphasis. Clearing every collected input restores normal sketch colors and candidate region shading. OK and Cancel remove all temporary emphasis and restore prior display state. Do not persist temporary colors or create document geometry for highlighting. Preserve native edge and interior-region picking, validation and geometry semantics; WORK_STATE records verification and delivery.

### D2859

Component operation entry: starting Extrude or another component operation automatically displays the active component's History tab as its creation task opens. This applies to the shared Sketch, Extrude, Revolve, Loft, Pipe, Helix and Primitive workflows, including entry from Models or Part Tree. If the Components panel is hidden, reveal it. Preserve profile preselection, the active component and occurrence context, and return to the original component view on OK or Cancel. History editing continues to use the same task. Verification and owner delivery are recorded separately in WORK_STATE.

### D2860

Curve-list interaction: in every shared component modeling curve collector, highlight and scroll to the most recently picked curve in the task list. Picking a collected curve again removes it and leaves no row highlighted. Give the curve list keyboard focus after a viewport pick so Delete removes its highlighted entries immediately; Delete with no highlighted entries does nothing and never deletes the source sketch. Apply the same behavior to Extrude, Revolve, Helix, Loft and Pipe profile curves and Pipe sweep/auxiliary path edges. Remove the redundant Add selected curves, Add selected and Use selected capture buttons; retain automatic collection, preselection, Remove, Clear, Use all/Use whole and the explicit Pipe path-role picker. Region picking continues to collect the complete boundary and highlights its last collected entry. Keep persistent viewport emphasis for the remaining collected curves, preview validation and OK/Cancel restoration. WORK_STATE records runtime verification and owner delivery. A click within the native edge-picking tolerance must select only that edge, even in a tilted view where the edge hit is slightly behind the sketch-plane intersection. The same click must never also collect a closed region. Interior clicks away from edges continue to collect complete region boundaries. Use one reusable source/list/action component for profile curves, Loft/Pipe section curves and Pipe sweep/auxiliary path edges, with shared selection and display handling.

### D2861

Combined owner build and cleanup, October 3: incorporate the current component modeling changes in one new portable owner build, including task-entry History, curve-list highlight/toggle/Delete behavior, persistent curve emphasis and sketch dimming, compact vertically scrolling tasks, sketch-region picking, grid-off default and ribbon panel styling. Rebuild all enabled targets using the existing configured compiler tree and label this an incremental rebuild with new staging. Preserve the configured workbench scope and native geometry. Validate the staged Plus launcher, its native/source identities and the desktop shortcut before handoff. Remove obsolete FreeCAD outputs from D:\Temp\Office-PC after preserving historical reports, scripts and CAD fixtures in verified archives. Retain the active compiler tree, reusable dependencies and any folder used by a running application. WORK_STATE records the build, runtime checks, cleanup results and publication separately; physical owner acceptance remains separate. Follow-up temp cleanup also removes confirmed empty temporary folder trees and superseded build/test folders after preserving historical evidence. Retain the current owner build, its immediate rollback build, active applications, reusable build tools and dependencies, and folders whose obsolescence cannot be established. Verify resolved paths remain inside the requested temp folder and do not follow reparse points. WORK_STATE records the removed scope and verified evidence archive.

### D2862

Modeling preview types: Extrude, Revolve, Loft, Pipe, Helix and Primitive use a dropdown with None, Overlay (default) and Result. Automatic updates remain enabled by default. Once the required closed profile and other geometric inputs are complete, Overlay shows the full native tool in blue for New Body, green for Add or red for Subtract. Add/Subtract overlays do not require a target or Boolean intersection and are not clipped to the target: a 5-inch subtract extrusion remains 5 inches long through a 1-inch body. Reference-defined extents still require their geometric references. Result shows the evaluated final geometry in normal body appearance without operation colors; it requires valid targets and a valid result. None removes the preview. Switching types, failed previews and Cancel restore prior visibility and transparency; collected curves retain their task highlights. OK continues to validate the actual operation and preserve native geometry, undo and persistence. WORK_STATE records native runtime acceptance, Python-only owner staging and shortcut delivery separately. Share the preview controls and debounce timer across all six tasks. Reuse common operation/target choices, compact layouts, reference rows, quantity fields, refinement/fuzzy-tolerance options and status controls wherever applicable; keep operation-specific geometry, native properties and validation in their existing backends.

### D2863

Components panel double-click editing: in History, double-click an operation or feature name, icon or status area to open its existing edit task; double-click a sketch to enter Sketcher edit mode directly. Editing must still work if a document notification rebuilds the History rows between the clicks. Resolve the selected document object before opening the editor, preserving the component and occurrence context. Keep single-click selection, visibility eyes, suppression checkboxes, Models and Part Tree component editing, and context-menu Edit unchanged. Origins remain protected and another active task must be finished before opening a different editor. Closing or cancelling the editor returns to the original component context. WORK_STATE records native mouse-input regressions, owner-build delivery and documentation review separately.

### D2864

Model History ordering: drag feature/object names, icons or status areas to reorder within the active component. Drop above or below a row; empty space means the end. Clamp an invalid drop to the closest valid position after all predecessor objects and before all dependents, following transitive geometry and expression dependencies, including hidden profile binders and published results. The native part Origin remains the first displayed item and cannot be dragged; its origin planes remain protected. Dropping near the origin places a movable item at its earliest legal position below it. Multiple selected items retain their existing relative order, as do unselected items; an intervening dependency remains between selected items when needed. Show the actual allowed insertion line and scroll long histories at viewport edges. Store the change as one undoable History-order edit, preserving geometry, links, object/result identities, ownership and save/reopen behavior. Background results travel with their visible producer. Refuse cross-component, stale and active-edit moves. Keep existing selection, double-click editing, visibility and suppression behavior. WORK_STATE records verification and owner delivery separately.

### D2865

Editing Model History: temporarily suppress every subsequent feature or object in the active component, following the current reordered History sequence. Editing item 5 of 10 suppresses items 6 through 10, including independent later items and their background results. Keep the edited item, earlier items and native Origin available. Apply this shared behavior to sketches, native feature editors and combined modeling tasks. Later items show an unchecked Suppressed during edit state, are hidden and are unavailable as evaluated component inputs or results until editing ends. Keep existing authored suppression unchanged. Accept or Cancel restores prior suppression and display choices; a failed validation keeps the edit and temporary suppression active, while failed editor startup restores them. Refresh downstream results after completion. Temporary state must not create an Undo entry, alter object identities or persist when saving during an edit. Preserve component and occurrence context on return. WORK_STATE records native runtime checks, Word review and owner delivery separately.

### D2866

Design selection toolbar: show alongside Save and Edit above the ribbon, only in Plus UI Design mode. The first dropdown offers Single Curve (default), Connected Curves and Tangent Curves for drawing curves and body edges. The second dropdown contains independent checkboxes for Planes, Bodies, Surfaces, Faces, Edges, Curves, Points and Vertices. Keep command-specific input rules in effect; the filter must not replace or widen a task collector gate.

### D2867

Selection categories: Surfaces are sheets not associated with bodies; Faces and Edges belong to bodies. Curves are drawing items, including sketch curves and standalone three-dimensional curves such as isoclines. Points include sketch points, reference points and origins; Vertices are body corners. A sketch remains drawing geometry even when owned by or used to construct a body. Preserve full occurrence paths. A sheet boundary remains in the Surface category; solid result objects are selectable Bodies even when their native type is not PartDesign Body.

### D2868

Curve intent: Connected Curves follows endpoint connections within the picked sketch or shape, including every branch and closed multi-edge loop, without crossing separate objects. Tangent Curves follows endpoint-connected tangents and stops at branches or tangent discontinuities. Use 0.0000001 mm endpoint tolerance and 0.00001 radian tangent-angle tolerance, independent of zoom. A closed periodic curve remains one item; its parameter seam does not connect it to other curves. Sketch construction geometry retains its native geometry indices. Feature collectors retain ownership of their reference-picking behavior.

### D2869

Directional Selection defaults on and remembers the saved preference. Left-to-right selects only fully enclosed geometry; right-to-left additionally selects crossing geometry. When off, both directions require full enclosure. Use a solid enclosure border and a dashed crossing border, consistent in sketch edit and the three-dimensional view. Both directions obey enabled entity filters and command input rules. Native projected bounds and tessellated geometry determine enclosure and crossing; hidden objects remain excluded.

### D2870

Persistent Selection defaults on and remembers the saved preference. Identity-preserving operations retain surviving selected entities so Equal can be followed by Construction Geometry without reselecting the same lines. Failed operations keep inputs available for correction; deleted entities leave selection. Turning persistence off restores operation-completion clearing. Escape and clicking empty space deselect all items even with persistence on. Do not restore stale subelement indices after topology changes or override deliberate command-collector resets. The constraint palette and Move Components task use the same preference.

### D2871

Selection toolbar validation: final October 6 packaged acceptance passes all 19 selection checks on this fork, without application source overlays. Actual native viewport picks, connected/tangent modes, directional boxes, taxonomy, command persistence, Escape and empty-space events are tested at system DPR 1.5 and DPR 3.0. Escape also clears the late native parent reselection after edit teardown; the originating document, active Design lifecycle and event generation guard every deferred checkpoint. A later viewport, tree, palette or control click supersedes that clear. Physical owner feedback remains separate; WORK_STATE records exact evidence.

### D2872

Design Layers: Each document has permanent Base and exactly one active layer, initially Base. Base cannot be renamed or deleted. Origin and origin features always belong to Base. New independent model objects take the active layer; missing or foreign assignments in an existing document migrate to Base. Layer IDs, labels, visibility, active choice and assignments are native saved properties, with undo/redo. Layer metadata has NoRecompute semantics and introduces no document dependency links.

### D2873

Design Layers: A sketch is indivisible and remains independent of every body that consumes it, including a sketch nested in a native Body. A Body and its building operations share a layer. Native Body membership and explicit Plus Producer/ConsumedResults relationships define the body unit; arbitrary dependency recursion is forbidden. Selecting several operations of one body resolves to one assignment owner. Sketch selection moves only that sketch. New operations inherit their existing body's layer. Same-document occurrences resolve the shared definition's model objects; external definitions are edited in their owning document, not implicitly reparented.

### D2874

Design Layers: The Design-only Layers toolbar sits beside Selection/Save/Edit. It contains Layers (open task panel), Move to Layer and Change Active Layer. The latter two are compact fixed-label whole-button menus, not split buttons or current-value combo boxes. Move to Layer is disabled without eligible preselection and changes all deduplicated targets in one transaction. Active-layer menu items show the current check mark.

### D2875

Design Layers: The task panel creates, renames, deletes, assigns and activates layers. Double-click a layer to activate it; active text is bold with a check. An eye control toggles each row's visibility. Layer hiding gates scene geometry without changing individual Visibility properties or taking snapshots. Hidden intermediate results remain hidden, individual changes while hidden are respected, and independently layered sketches remain traversable in the Body's native Group display. Native container Visibility and native Through/Tip display choices continue to govern their own scene traversal. Delete moves assignments to Base, never deletes geometry, and activates Base when the deleted layer was active. Changes are individually undoable from the task panel.

### D2876

Contextual Constraint Palette: Only a click while editing a sketch in Plus Design mode opens the palette. Use the entire native selection, including additional selection clicks; box or programmatic selection alone never opens it. Place above the click where possible, otherwise below or clamp within the viewport. Use logical pixels for DPI scaling. Keep a 24-pixel-wide travel corridor to the actual palette rectangle, with a 12-pixel anchor allowance and a 4-pixel palette margin. Remain visible indefinitely inside; outside starts a one-second grace timer and reentry cancels it. New clicks restart the travel context. Action updates retain position unless viewport clamping requires movement. Dismissal by pointer travel leaves selection intact. Choosing an action removes its native tooltip frame immediately, before solving. Refresh and close hide retired controls immediately; native icons, hover text and the one-second pointer-travel grace remain unchanged.

### D2877

Contextual Constraint Palette: The palette contains only applicable native constraints/dimensions, Construction Geometry and separate Make Driving/Make Reference actions. Display icon-only buttons using each corresponding native toolbar action icon and the exact native hover tooltip, including translated descriptions and shortcuts. Follow native icon and tooltip changes. Retain separate accessible names and the existing batch behavior for Make Driving and Make Reference. Structurally inapplicable actions are absent. Existing constraints and known conflicts/redundancies remain disabled. Show the unchanged native tooltip on disabled buttons too; show the palette-specific reason in the status bar on hover and retain it as the accessible description. A cloned native Sketch solver diagnoses additions without changing committed geometry, constraints or the live solver. Nonconvergence alone is unknown feasibility and does not disable an action. No hover action adds constraints. Revalidate the live sketch and full selection before execution; native dimension dialogs retain their normal units and command safeguards.

### D2878

Contextual Constraint Palette: Mixed construction selections become all normal, then all construction. Uniform selections toggle together. Dimension states are separate from construction flags. Dimension conversion validates all inputs, applies one native batch and solves once, as one undoable change. Preserve constraint order, names, identities, values and expressions. Making an expression-driven dimension reference is disabled because native conversion would remove its expression; the user must explicitly remove that expression first. Native external-only driving restrictions remain in force.

### D2879

Contextual Constraint Palette: Make Driving is allowed even when the solver reports a conflict or invalid sketch. Commit that converted state, retain the native diagnostic, and allow one Undo of the whole batch. An API/input failure aborts the batch; it is not a committed invalid solve. Other invalid constraint additions abort normally. Persistent Selection on retains native surviving selections and updates the palette in place. Off clears selection and closes the palette after success. Escape and empty-space clicks clear selection and close it in either state. Clean up on sketch exit, document close, deletion and task/mode changes. No repair feature is introduced here.

### D2880

Layers and contextual palette validation: final October 6 packaged acceptance passes ten Layers and fourteen contextual palette checks on the grouped native fork at system DPR 1.5 and DPR 3.0, without application source overlays. Tests cover metadata/history and independent input sketches, real pointer/corridor timing, compact placement, disabled tooltips, Equal/Construction persistence, native cloned-solver diagnostics, atomic driving/reference batches and committed-invalid driving Undo. The owner DOCX is synchronized, rendered and reviewed. Exact runtime identities, grouped build and desktop launch delivery evidence are recorded in WORK_STATE. Physical owner feedback remains separate.

### D2881

Move Components: Move Components opens one Tasks panel from Design Assembly or the Part Tree instance context menu. It moves whole linked component instances and their descendants. Models, permanent master/root contexts and geometry subelements are not movable instances. Copy remains a separate Part Tree operation. The first field is Workflow, ordered Translate, Rotate, Point to Point, Align Axes, Align Coordinate Systems, Interactive. All six workflows pass final October 6 grouped native and packaged acceptance. Exact test-build and desktop shortcut launch delivery evidence is recorded in WORK_STATE; physical owner feedback remains separate.

### D2882

Move Components: The next control is the Components list, using the existing add-selection, Remove/Delete and Clear collector conventions. The first valid batch establishes the immediate parent definition and its exact displayed occurrence path as the active editing context. Only direct siblings under that same displayed parent are accepted; mixed batches are rejected in full with inline explanation. Descendants are implicit and receive no second placement change. Clearing the list retains the parent context. Ordinary component clicks outside the task do not activate parents. External parent definitions must be opened in their owning file.

### D2883

Move Components: A parent definition owns its children's relative LinkPlacement values. Moving children changes them in every occurrence of that parent, including its standalone component tab. Preserve the selected parent occurrence path for reference conversion; do not create a display-path placement override, reparent links, copy definitions or change source shapes/history. The task displays this shared-parent consequence. Driven, read-only, grounded and relationship-owned instances are refused, including native assembly joint references that traverse a root plus a deep subpath.

### D2884

Move Components: Translate uses one normalized direction, one nonnegative unit-aware Distance and a Reverse toggle, initially direction unset, zero length and Reverse off. Directions are Parent X, Parent Y, Parent Z or a picked straight edge, line/reference axis from visible geometry. Picked occurrence/world vectors transform by the inverse parent rotation only; parent translation does not affect a direction. Reject curved, undefined, zero or ambiguous bare shared references. Snapshot the direction without adding associative dependencies. All selected siblings receive the same parent-frame rigid transform. Reverse changes sign while retaining Distance.

### D2885

Move Components: Teal, non-pickable geometry previews intended placements without writing document properties or creating document objects/undo records. Show the effects in every displayed occurrence of the shared parent, using each occurrence's native frame. Apply commits all siblings in one transaction and keeps the panel open. It resets Direction, Distance and Reverse; Persistent Selection on retains the list/highlights, off clears both. No-op Apply creates no undo record. OK applies a valid nonzero pending move and closes; after Apply it simply closes. Cancel discards only the pending preview, retaining earlier Apply transactions for Undo. Switching workflows discards uncommitted parameters/preview while retaining siblings and parent context.

### D2886

Move Components: Errors remain inline in the task. A changed parent or selected placement invalidates the pending preview and requires Reset movement inputs; stale placements are never silently applied. Selection changes and removals reset movement inputs. Close the task and release observers/preview on document or component-view exit; deleted instances leave the list, and deletion of the parent context closes the task. All six workflows require native/packaged acceptance before owner delivery; WORK_STATE records source-overlay evidence and DOCX rendering status.

### D2887

Move Components: Rotate uses Parent X/Y/Z through the parent origin, a picked straight line with its location and direction, or two distinct points. An optional picked pivot relocates a parallel axis. Vertex, native sketch/reference point, origin and analytic circle center picks retain their displayed occurrence transforms. Angle is a finite magnitude from 0 to 360 degrees; positive follows the right-hand rule and Reverse negates it. Rotate applies one common rigid delta to sibling positions and orientations. The transient preview labels the parent-frame pivot, positive axis and signed angle. Apply clears axis, pivot and angle and turns Reverse off. The recovered Rotate implementation and eight updated tests are retained. October 6 native and packaged Plus runs pass all eight Rotate and twelve Translate checks, including Undo/Redo and FCStd/cadprt reopen; installed Rotate task captures are visually reviewed. Recovery item 1 is complete. Recovery items were executed through separate owner prompts; final grouped native/packaged acceptance and saved desktop shortcut launch pass in item 7. Physical owner feedback remains separate.

### D2888

Move Components: Point to Point snapshots a Source and Destination vertex, sketch/reference point, origin or analytic circle center from any visible displayed occurrence. The Source need not belong to the moved group. Convert both to the active parent frame and translate every sibling by Destination minus Source, preserving orientations, group spacing and descendants. Show labeled points and distance with transient markers/vector; no joints, constraints or lasting references are created. Coincident points create no undo entry. Missing, invalid or deleted references prevent Apply. Apply clears both point inputs; selection follows Persistent. Reset/method switch/Cancel remove pending preview. All four cases pass final native packaged acceptance, including no-op, reference conversion, Undo/Redo and save/reopen. Final grouped build and saved desktop shortcut launch pass; physical owner feedback remains separate.


### D2889

Move Components: Align Axes snapshots Source and Target straight/reference axes, analytic circular axes or cylindrical-face axes through exact displayed occurrences. Default Make Coincident uses minimal-angle rotation and maps the Source anchor to its closest point on the Target axis; Make Parallel rotates about and retains the Source anchor. Reverse Target Direction explicitly negates Target. Opposite directions use Source cross the least-aligned parent X/Y/Z basis, with X winning ties, for a stable 180-degree rotation. Show resolved Source/Target direction arrows and transformed Source; all siblings receive one rigid parent-frame delta. Apply clears picks and restores Coincident/Reverse-off defaults. No joints, associations or arbitrary axial slide. The earlier packaged Plus run passes five native regression cases. The separate item 3 review strengthens those cases with parallel/coincident no-op, deterministic antiparallel roll, repeated baseline previews and FCStd/cadprt placement round trips. These strengthened assertions pass all five native packaged cases in final recovery item 7, including shared occurrence updates, parent-owned sibling/descendant persistence and Undo/Redo. Grouped build, DOCX visual review and saved desktop shortcut launch pass; physical owner feedback remains separate.

### D2890

Move Components: Align Coordinate Systems maps a complete Source rigid frame to a complete Target frame, including origin and roll, with one Target times inverse Source delta shared by siblings. Pick existing native component origins/datums, explicitly choose Parent, or expand Origin/Z/X definitions. Normalize Z, project X perpendicular to Z and derive right-handed Y. Reject zero/parallel directions and scaled, sheared, reflected or nonfinite frames. Show Source/Target triads and origins, without exposing matrices. Picks snapshot displayed occurrences against unchanged geometry; Apply clears definitions and references, and Cancel removes only pending preview. The earlier packaged Plus run passes five native regression cases, including full roll alignment, displayed occurrence frames, scale/reflection rejection and native Undo/Redo/save/reopen. Separate recovery item 4 strengthens those cases with repeated baseline previews, both displayed parent orientations, OK-after-Apply non-repetition, sibling/descendant round trips and preview/Cancel preservation. These strengthened assertions pass all five native packaged cases in final recovery item 7, including shared occurrence updates, parent-owned sibling/descendant persistence and Undo/Redo. Grouped build, DOCX visual review and saved desktop shortcut launch pass; physical owner feedback remains separate.

### D2891

Move Components: Interactive uses the existing native translation arrows, plane handles and rotation rings, aligned initially to the active parent. Default pivot is the selected group parent-frame bounds center, with mean selected origins as the nongraphic fallback. Separate Move Components from Edit Pivot; relocating/orienting the command-local pivot never changes geometry or adds Undo. Point, origin, circle-center and edge-midpoint picking, explicit axis/frame orientation and Reset Pivot are available. Gestures compose against unchanged placements and mouse release retains preview. Apply atomically commits siblings, clears movement/pivot inputs and restores the default pivot for retained selection, or removes handles when Persistent is off. Escape during drag restores that gesture baseline and releases capture before broader selection handling. Numeric active-handle gestures and explicit distance/angle snapping are available; snapping defaults off. Task/method/mode/document exit removes capture, callbacks and handles. The earlier packaged Plus suite passes five native regression cases; the DPR 3.0 focused rerun also passes five, including real mouse drag/release, Escape and pivot-edit events. Its fixture pans only the camera and ray-picks visible unobscured native handles, without writing component placements or pivot state. Separate recovery item 5 adds native plane/ring event checks, default parent-aligned pivot recreation after Apply, OK non-repetition and sibling/descendant Undo/Redo/FCStd/cadprt round trips after actual gestures. The strengthened five-case suite passes final native packaged acceptance at system DPR 1.5 and DPR 3.0, including real axis, plane, ring and movable-pivot events, retained release preview, gesture Escape, camera navigation, Apply/OK reset, sibling/descendant Undo/Redo and FCStd/cadprt round trips. Final DOCX and saved desktop shortcut launch gates pass; physical owner feedback remains separate.

### D2892

Move Components: October 6 native acceptance repairs retain exact parent-owned sibling placements and the approved six workflows. Native mapped sketch tokens resolve to their owning occurrence before Connected/Tangent expansion. Bare component frames resolve through the displayed native Origin and scaled links fail rigid-frame validation. Interactive numeric controls validate only the active arrow/plane/ring inputs; pivot pick/reset changes cancel superseded guards. Native dialog auto-close on owning-document deletion cleans observers, preview and handles without late document lookup. Focused installed native evidence passes Selection 18/18, Interactive 5/5, palette 14/14 and integration 5/5 with real viewport and handle events, no overlays or skips. The grouped native build and final packaged acceptance pass: 89 full checks, 55 checks at DPR 3.0 and 26 smoke checks launched through the saved desktop shortcut. The native capture repair produces the reviewed opaque framebuffer. WORK_STATE records exact snapshots and payload identities; physical owner feedback remains separate.

### D2893

Move Components: native visual acceptance requires a fully rendered live Qt framebuffer, including handles and overlays. The inherited deferred-redraw limiter left capture framebuffers unpainted; native paintGL now renders these synchronously while ordinary viewport requests keep their frame-rate limit. Automatic-redraw state is restored on exit. The seven native integration checks pass, including live opaque-face pixels, actual Design Assembly tab/button events, the Part Tree Move action, six compact tasks, outside-parent picks, external-parent enforcement and document lifecycle cleanup. The repaired screenshot is visually verified. Full 89-check packaged, 55-check DPR 3.0 and 26-check saved desktop shortcut launch acceptance pass; WORK_STATE records exact logs and runtime identities. No placement, geometry, ownership, selection default or physical acceptance contract changes.


### D2894

Recovery item 6 integration reconciliation retains Selection, Layers, Contextual Constraint Palette and all six Move workflows. Deferred Escape clearing checks the originating event generation, active Design lifecycle and document again inside the final queued callback; native cancellation remains unconsumed and a later click must survive. Sketcher diagnostics clone geometry/constraints, while committed-invalid driving batches retain their converted state for Undo. Layer metadata and visibility gates preserve independent input sketches, identities and geometry. The existing native build and earlier packaged 88-check evidence remain historical to their source/test snapshots. Current quick checks pass eight Python syntax checks and four controlled deferred-callback orderings; these do not establish Qt/native runtime acceptance. Recovery item 7 executes the updated 89-check full suite, 55-check DPR 3.0 subset and 26-check saved desktop shortcut smoke, without overlays or skips. Actual handle/collector events, Undo/Redo, both saved formats, lifecycle cleanup, final DOCX review and launch verification pass. Item 6 remains a source milestone; item 7 delivers the grouped incremental test payload. Deferred feature families remain deferred.

### D2895

Recovery item 7 native fixture reconciliation: the Selection click fixture uses geometry away from the overlapping sketch H-axis, refreshes actual hover and separates independent single-click cases. Native handle fixtures use the actual renderer viewport and a zero-tolerance interior patch of each handle, preserve the real cursor/motion stream and separate single drags. They do not substitute placement or pivot writes for interaction. Selection passes 19 checks; Interactive passes five, including axis/plane/ring and Edit Pivot events, Escape, retained release preview, camera navigation, Apply/OK reset, Undo/Redo and FCStd/cadprt sibling/descendant round trips. Unsuccessful finish/cancellation hypotheses and diagnostic application instrumentation were removed; the retained application behavior is unchanged by these fixture repairs. Final combined 89-check, 55-check DPR 3.0 and 26-check saved desktop shortcut delivery gates pass. High-DPI event fixtures settle layout, dismiss an intercepting native notification through actual clicks, verify an unobscured viewport, assert unchanged sketch geometry and expose the native Z ring with a camera-only top view. Late Escape clearing is guarded at every checkpoint and later deliberate clicks survive. Native binaries are reused from the verified grouped build; refreshed packaged Python/resources are identified separately from the embedded compiled revision. This is a local test-build delivery; physical owner feedback remains separate.

### D2896

October 6 archival publication: the original October 3 ten-prompt workload backups and queue receipts are retained as a historical archive. Recorded prompt hashes match the saved files. These receipts do not establish execution or submission of the recovered seven prompts in this conversation. The delivered native test payload retains its validated b75ba0252f source snapshot. This archive changes no UI behavior, geometry, defaults or build. WORK_STATE retains current acceptance evidence; archive copies must not be executed or enqueued again.

### D2897

October 6 sketch-edit selection correction: in Plus Design, a plain point/edge/constraint click replaces the selected item; a repeated plain click retains that item. Ctrl or Shift permits native multi-selection. A plain empty-space click clears selection, while Ctrl/Shift empty clicks retain it. Persistent Selection controls retention after operations and must not turn plain clicks into multi-selection. Dragging, box selection, context-menu picks and Classic native behavior retain their own semantics. Palette feasibility checks use cloned solver data and must not report errors or warnings for unapplied hypothetical constraints. Quiet handling belongs only to that probe; actual modeling/constraint operations retain native diagnostics and Undo behavior. Both defects reproduce on the preceding delivered build: two plain point clicks accumulate selection, and the hypothetical coincidence of a line's endpoints repeatedly reports failed solvers and geometry errors. Rebuilt native acceptance: the grouped Release/x64 ALL_BUILD passes after incremental continuation of the first wrapper deadline; 66 rebuilt native binaries are staged and hash-verified. All 18 packaged native palette checks pass, plus three focused checks at increased Qt scale and three checks launched through the saved desktop shortcut. Actual point clicks, Ctrl/Shift and empty-space behavior, quiet hypothetical probes, retained live-operation diagnostics, native point dragging, Undo/Redo and FCStd save/reopen pass without application source overlays. The existing desktop shortcut target and working directory are reopened and verified. A separate Design-selection audit passes 18 of 19 checks; its unobscured-viewport hit-test returns no widget despite a visible/exposed window and remains unqualified. This does not establish broad workbench or physical owner acceptance. WORK_STATE records exact evidence, provenance and the remaining validation step.

### D2898

October 6 medium ribbon icon enlargement: medium icons increase from 20 to 32 logical pixels and buttons from 38 to 42 pixels high, retaining two rows in the shared minimum 86-pixel grid. Medium/small buttons stay icon-only with native artwork, tooltips, action state and accessibility; large captions and gray group dividers are retained. Five installed native checks, two DPR 3.0 checks and two actual saved-desktop-shortcut checks pass without source overlays. Native paint captures confirm larger glyph area without clipping, all seven Design tabs are checked, and actual Box-button/Cancel preserves object identities. Native binaries and the preceding sketch-selection/quiet-probe fixes are reused unchanged. The owner DOCX render/inspection and final publication are recorded in WORK_STATE.

### D2899

When a legacy file opens, Models lists its part definitions and Part Tree shows linked instances beneath the pinned file row. Repeated instances reference the same model. Review legacy conversion explains incomplete mappings, missing instances and any geometry-only recovery. Label recovered outputs as recovered geometry and explain that their parametric history has not been converted. Missing instances remain visible for repair. Save converted external parts as new .cadprt files before the parent, leaving legacy originals untouched. For supported simple Sketch and Pad histories, History lists the sketch, Pad operation and original Body result in that order, preserving their labels. Double-click the sketch to edit its constraints or Pad to open the Extrude task. Repeated instances update from the shared model. Review legacy conversion identifies histories that remain native and editable. Retained expressions use the property editor; operation and target changes reject downstream self-references and preserve the original feature identity. Legacy datum planes, axes, points and coordinate systems retain their labels and native attachment settings. Body-owned datums appear as hidden links in component History. Double-click opens the original attachment editor; Cancel preserves supports and offsets. Retained planes are available to New Sketch and follow their native offsets and frame changes. Missing or invalid datum sources show Needs repair. Origins and their planes keep their existing names and permanent controls. Retained Body-owned sketches appear as hidden links before their Body in History. Double-click edits the original sketch and its existing constraints; all consumers and repeated instances use that same sketch. Existing attachments, external references and expression-driven dimensions remain editable in their native controls. Missing or invalid sketch sources show Needs repair; repair the original input before using it.

### D2900

Supported legacy Pad and Pocket chains appear in History as independent sketches and Extrude operations with explicit target bodies, ending in the original Body result. Double-click a converted Pocket opens the shared Extrude task with Subtract, its existing target and the correct direction selected. Accept updates the operation; Cancel leaves its saved parameters and target unchanged. Existing expression-driven parameters remain available in the property editor. Converted Pad/Pocket modes and targets can be edited while keeping the original feature. Standalone native Part Extrusion retains New Body; create a separate operation to change its operation kind. Retained native Pad/Pocket histories appear as hidden History links; double-click opens the original native editor with its attachments and extent references intact. Missing or invalid retained operation sources show Needs repair. Supported independent Part Extrusions also open in the shared task; custom direction, taper and sheet or curve outputs retain their native controls.

### D2901

Supported legacy Revolution and Groove histories show their original sketches, Revolve operations, target bodies and final Body in History. Double-click opens the shared Revolve task with saved axes, angles, direction and signed start offset. Accept updates the operation; Cancel preserves saved settings. Preview follows rotated sketches and construction axes. Converted features retain their native Revolution or Groove type; create a separate operation to switch additive/subtractive type. Formulas remain editable in properties. Attached or reference-dependent histories and standalone Part Revolution retain their native editors and signed-axis controls. Missing or invalid retained sources show Needs repair. Review legacy conversion distinguishes mapped operations from retained native histories. Undo/Redo restores conversion and edits without stale component views.

### D2902

Supported legacy Lofts show their original section sketches before Loft operations, explicit target bodies and the final Body in History. Double-click opens the shared Loft task with sections in their saved order and existing Smooth/Ruled, Closed, Refine and tolerance settings. Preview section reorder or replacement before Accept; Cancel preserves saved sections and targets. Converted Loft modes and targets can change while keeping the original Loft. Vertex end sections retain their picks. Formula-driven settings use properties. Attached histories, native Common operations and legacy sketch-edge references that mean the whole sketch retain the original native editor. Standalone Part Loft retains its native degree, linearization and solid/sheet controls. Missing or invalid retained sources show Needs repair. Undo/Redo restores conversion and edits; repeated instances update from the shared model.

### D2903

Supported legacy Pipes show their original profile sections and path sketches before Pipe operations, explicit target bodies and the final Body in History. Double-click opens the shared Pipe task with saved section order, path and auxiliary edge picks, orientation, corner transition and Constant/Multisection settings. Preview changes before Accept; Cancel preserves saved references and targets. Converted Pipe modes and targets can change while keeping the original feature. Formula-driven settings use properties. Attached or unsupported histories, native Common operations and whole-sketch edge references retain the original native editor. Standalone Part Sweep retains its native solid/sheet, Frenet and linearization controls. Missing or invalid retained sources show Needs repair; unavailable selected path edges give a repair message. Review legacy conversion identifies stale outputs requiring recompute. Undo/Redo restores conversion and edits; repeated instances update from their shared model.

### D2904

Supported legacy Helix histories show original profiles before Helix operations, explicit targets and the final Body in History. Double-click opens the shared Helix task with saved parameter mode, pitch, height, turns, cone angle or growth, axis, handedness and direction. Preview changes before Accept; Cancel preserves saved settings and references. Converted modes and targets retain the original Helix feature. Formula-driven parameters remain editable in properties. Attached or unsupported axes and histories retain their native editors and available geometry. Standalone Part Helix retains its native curve controls. Review legacy conversion identifies unverified output requiring recompute; missing retained sources show Needs repair. Undo/Redo restores conversion and edits; repeated instances update from the shared model.

### D2905

Supported legacy Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism and Wedge histories show Primitive operations with explicit targets and the final Body in History. Double-click opens the shared Primitive task with the saved shape, native dimensions and placement. Preview changes before Accept; Cancel preserves saved settings. Converted Add/Subtract/New Body modes and targets retain the original primitive; create a separate operation to change its shape type. Formula-driven dimensions use properties. Attached or unsupported histories retain the original native editor. Standalone Part primitives retain their native controls. Review legacy conversion identifies stale or unavailable output; missing retained sources show Needs repair. Undo/Redo restores conversion and edits; shared instances update together.

### D2906

Legacy Fillet, Chamfer, Draft and Thickness operations appear in component History while retaining their native Body and selected faces or edges. Double-click opens the original native editor with saved settings. Standalone Part dress-ups retain their original controls and outputs. Missing or invalid retained sources show Needs repair; Review legacy conversion identifies unverified output requiring recompute.

### D2907

Legacy patterns and transformations appear in History with referenced inputs before consumers, retaining authored order where compatible. Double-click opens the native editor with saved originals, direction or axis references and transformation settings. MultiTransform preserves its ordered transformations; combined Pattern retains both Linear and Circular settings and suppressed copies. Boolean History opens the original native editor with its saved operation, target and tool Bodies. Native owners and geometry remain retained; these operations are not presented as newly flattened shared operations. Undo/Redo restores conversion and edits; saved files preserve the original model shared by repeated instances.

### D2908

Open legacy FCStd files through File > Open. Models contains definitions, Part Tree contains linked instances, and History shows inputs, operations and finished results. Mapped operations use the shared task; retained operations open their original native editor. Save converted content to a new cadprt file, saving external definitions before their parent. Legacy originals remain protected. Missing definitions remain visible; right-click and choose Locate Component File to repair them before saving. Review legacy conversion identifies retained native histories, unverified caches and explicit dumb geometry recovery. Geometry-only recovery preserves available output while reporting loss of parametric component editing. Repeated instances share model edits; instance placements remain independent. Conversion and geometry-only recovery both add the pinned file row, with its global Origin, above the converted domestic component. Recovered outputs belong to that component; the file has no modeling geometry. The file row is excluded from Models. One Undo reverses the entire conversion, including the file container, and Redo restores it. No additional Part001 is created.

### D2909

Inherited interface requirements: the TechDraw face-color preference explains that it affects projected faces; existing saved colors remain respected. The Start Page must not leave an overlay dock covering its content, and overlay menu colors follow the active theme. Sketch editing preserves the saved non-edit toolbar layout. Closing a document removes its task dialog and any attachment or feature-picker callbacks.